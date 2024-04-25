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
from datetime import datetime
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
alerts = database.child("Alerts").get().val()

'''
This function checks the queue and processes the remaining elements
'''

def processCheckQ():
    while carnetQ:
        # Processing Images
        Obj = carnetQ[-1]
        carnetQ.pop(-1)
        Obj.downloadImg(Obj.photoURL)
        Obj.results = Obj.getCarnetResults()
        print(Obj.results)
        #Send results
        database.child(f"UserData/{Obj.UID}/submissions/{Obj.subID}/status").update(Obj.results)
        #Updating Location/Adding points
        Obj.processMatch(Obj.alertID)
        # Remove Object, garbage collector.
        print("Finished processing", Obj.UID)

'''
Class to process photo submissions
'''

class submissionProcessor:
    def __init__(self, UID, photoURL, alertID, subID): 
        self.UID = UID
        self.subID = subID
        self.photoURL = photoURL
        self.results = None
        self.alertID = int(alertID)
        carnetQ.insert(0, self)

        processCheckQ()
        
    def updatePoints(self, points):
        if points != None:
            userP = int(database.child(f"UserData/{self.UID}/points").get().val())
            database.child(f"UserData/{self.UID}").update({"points": points + userP})

    def getCarnetResults(self, photo="carnetImg.jpg"):
        response_json = rtx_veh_det.get_car_details(photo)
        formatted_text = rtx_veh_det.format_response(response_json)
        os.remove("carnetImg.jpg")
        return formatted_text

    def processMatch(self, alertID):
        if alertID == 0:
            print("Not Alert")
            pass
        else:
            alertObj = AmberAlert.objects.get(id=alertID)
            alert = AlertSerializer(alertObj)
            prevUser = alert['recent_Interaction'].value
            if not prevUser:
                print("prev")
                userP = int(database.child(f"UserData/{prevUser}/points").get().val())
                updateUserP = database.child(f"UserData/{prevUser}").update({"points": 50 + userP})
            if(self.results['Success']):
                if((alert['vehicle_color'].value == self.results['Color']) and (alert['vehicle_model'].value == self.results['Model']) and (alert['vehicle_make'].value == self.results['Make'])):
                    alertObj.alert_lat = database.child(f"{self.UID}/submissions/{self.subID}/data/lat").get().val()
                    alertObj.alert_long = database.child(f"{self.UID}/submissions/{self.subID}/data/long").get().val()
                    alertObj.recent_Interaction = self.UID
                    alertObj.save()
                    self.updatePoints(500)
            else:
                self.updatePoints(10)

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

        day = datetime.today().strftime('%#m-%#d-%Y')
        try:
            if((list(event.data.keys())[0]).startswith(day)):
                subID = list(event.data.keys())[0]
                url = event.data[f'{subID}']['photo']
                alertID = event.data[f'{subID}']['alert_id']
                UID = event.path.split('/')[1]
                submissionProcessor(UID, url, alertID, subID)
        except:
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
    usersFound = 0
    tokens = []
    # This loop interates through all User locations to determine if they are within range of the alert.
    for x in locations:
        try:
            print(x)
            Lat1, Long1 = locations[x]['last_location']['latitude'], locations[x]['last_location']['longitude']
            distance = m.acos( m.cos(m.radians(90-Lat1)) * m.cos(m.radians(90-Lat2)) + m.sin(m.radians(90-Lat1)) * m.sin(m.radians(90-Lat2)) * m.cos(m.radians(Long1 - Long2))) * 6371
            if distance <= 5:
                usersFound = usersFound + 1
                database.child(f"Alerts/{x}").update({f"Alert{alertID}": {'alertID': alertID, 'Region': alert['name'].value, 'car':{'make': alert['vehicle_make'].value , 'model':alert['vehicle_model'].value, 'color': alert['vehicle_color'].value}}, })
                tokens.append(x)
        except:
            pass
    sendToToken(alertID, tokens)
    print(f"Users found: {usersFound}")

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
    tokens = tokens
    )
    response = messaging.send_multicast(message)
    print(response)
    print("Alert sent!")
    return redirect('http://127.0.0.1:8000/')

def sendPing():
    #Retrieve All users and send notification to ping them.
    print("Pinging...")
    devices = database.child("Locations").get().val()
    tokens = list(dict(devices))

    message = messaging.MulticastMessage(
    notification=messaging.Notification(
    title = "Ping",
    body = "This serves to update the location!"
    ),
    data={
        'data': "Update your Location"
    }, 
    tokens = tokens
    )
    response = messaging.send_multicast(message)
    print(response)
    y = [print(x[0:10]) for x in tokens]
    print(f"{len(tokens)}... sent")