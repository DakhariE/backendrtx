from django.shortcuts import render, redirect
from django.db.models.signals import post_save
import math as m
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.decorators import api_view
from .serializers import AlertSerializer, ResultsSerializer
from .models import AmberAlert, UserResults
import pyrebase
from .keys import *
import firebase_admin
from firebase_admin import credentials, messaging, db, storage
import requests
import time
import os
from django.db.models.functions import Now
from . import rtx_veh_det

'''
This section initializes the firebase SDK
pyrebase is for accessig database
adminapp is for messaging.
'''
cred = credentials.Certificate(cert_key)
pyrebase=pyrebase.initialize_app(firebaseConfig)
try:
    firebase_admin.get_app()
except:
    adminapp=firebase_admin.initialize_app(cred, {'databaseURL':'https://rtx-alert-app-b343c-default-rtdb.firebaseio.com'})

#storage = adminapp
auth = pyrebase.auth()
database = pyrebase.database()
storage = pyrebase.storage()

'''
Variables containing Locations and UserData from firebase realtime database, and Queue to carnet.ai
'''

carnetQ = []
locations = database.child("Locations").get().val()
users = database.child("UserData").get().val()

'''
This function checks the queue and processes the remaining elements
'''

def processCheckQ():
    while carnetQ:
        Obj = carnetQ[-1]
        Obj.downloadImg(Obj.photoURL)
        Obj.results = Obj.getCarnetResults()
        findingUpdateLocation = database.child(f"UserData/{Obj.UID}/submissions").get().val()
        mostRecentSub = next(reversed(findingUpdateLocation))
        database.child(f"UserData/{Obj.UID}/submissions/{mostRecentSub}/status").update(Obj.results)
        carnetQ.pop(-1)
        print("Finished processing", Obj.UID)

'''
Class to process photo submissions
'''

class submissionProcessor:
    def __init__(self, UID, photoURL): 
        self.UID = UID
        self.photoURL = photoURL
        self.results = None
        carnetQ.insert(0, self)

        processCheckQ()

    def getCarnetResults(self, photo="carnetImg.jpg"):
        response_json = rtx_veh_det.get_car_details(photo)
        formatted_text = rtx_veh_det.format_response(response_json)
        os.remove("carnetImg.jpg")
        return formatted_text

    def updateLocation(self, UID):
        pass
    def updatePoints(self, number):
        pass
    def downloadImg(self,url, imgFile="carnetImg.jpg"):
        response = requests.get(url)
        if response.status_code == 200:
            with open(imgFile, 'wb') as file:
                file.write(response.content)
            return 200
        else:
            return 400

'''
This api send All alert data as a json
URL: 'http://127.0.0.1:8000/r/UID'
'''

@api_view(['GET'])
def sendAlert(request):
  alertList = AmberAlert.objects.filter(active=False)
  serializer = AlertSerializer(alertList, many=True)
  return Response(serializer.data)

'''
This function gets the data from a specific user based their username, should be changed to userID
'''

def getUserData(userName):
    return users[userName]

'''
This function updates Userdata in firebase database
'''

def updateUserData(UserID, score=None, result=None):

    return 200

'''
This function is called whenever there is an update in the Realtime database.
the event waits for an update in the UserData folder of the database.
then adds an instance of submissionProcessor to a queue.
'''

ref = db.reference("UserData")
def handle_added(event):
    # First listen call returns entire reference with path of / so we ignore it and wait for other calls.
    if event.path == '/':
        pass
    else:
        if len(event.path[1:]) == 28:
            UID = event.path[1:]
            url = event.data['latest_sub']
            submissionProcessor(UID, url)
        else:
            pass
ref.listen(handle_added)

'''
This Function is called whenever there is an update or create in the sqlite Alert database.
'''

def triggerEventSqlite(instance, *args, **kwargs):
    request = requests.Request
    if instance.active == True:
        filterAlert(instance.pk)

post_save.connect(triggerEventSqlite, sender=AmberAlert)

'''
This function intakes user location and calculates if a user is in a 5km radius.
'''

def filterAlert(alertID):
    alertObj = AmberAlert.objects.get(id=alertID)
    alert = AlertSerializer(alertObj)
    Lat2, Long2 =  float(alert['alert_lat'].value), float((alert['alert_long'].value))
    # This loop interates through all User locations to determine if they are within range of the alert.
    for x in locations:
        usersFound = 0
        Lat1, Long1 = locations[x]['last_location']['latitude'], locations[x]['last_location']['longitude']
        distance = m.acos( m.cos(m.radians(90-Lat1)) * m.cos(m.radians(90-Lat2)) + m.sin(m.radians(90-Lat1)) * m.sin(m.radians(90-Lat2)) * m.cos(m.radians(Long1 - Long2))) * 6371
        if distance <= 5:
            print(f"Users found: {usersfound}")
            sendToToken(alertID, x)

'''
This functions send the alert to a user based on their device token.
alert - An object represnting the details of an alert  
tokens - A string, representing a unique device iidentifier.
'''

def sendToToken(alertID, tokens):
    #Retrieve Alertdata and user token to send.
    alertObj = AmberAlert.objects.get(id=alertID)
    alert = AlertSerializer(alertObj)

    message = messaging.MulticastMessage(
    notification=messaging.Notification(
    title = alert['name'].value,
    body = "Silver alert Issued to X region."
    ),
    data={
        'alertID': str(alert['id'].value),
        'description': alert['description'].value,
        'date': str(alert['date'].value),
        'vehicle_model': alert['vehicle_model'].value,
        'vehicle_color': alert['vehicle_color'].value,
        'vehicle_make': alert['vehicle_make'].value,
        'vehicle_LP': alert['vehicle_LP'].value,
        'coords': str(alert['alert_lat'].value) + '|' + str(alert['alert_long'].value)
    },
    tokens = [tokens]
    )
    response = messaging.send_multicast(message)
    print("Alert sent!")
    return redirect('http://127.0.0.1:8000/')
