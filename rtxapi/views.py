from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.decorators import api_view
from .serializers import AlertSerializer
from .models import AmberAlert
import pyrebase
from .keys import *
import firebase_admin
from firebase_admin import credentials, messaging
import requests



# cred = credentials.Certificate(cert_key)
# pyrebase=pyrebase.initialize_app(firebaseConfig)
# adminapp=firebase_admin.initialize_app(credential=cred)


# auth = pyrebase.auth()
# database = pyrebase.database()
# storage = pyrebase.storage()

# # users variable is a dictionary of userdata from firebase.
# users = database.child("UserData").get().val()
'''
This api send All alert data as a json
URL: 'http://127.0.0.1:8000/alert'
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
    pass
'''
This function updates Userdata in firebase database
'''
def updateUserData(userName=None, location=None, score=None, URL=None):
    return 200
def filterAlert(alert, user):
    pass
'''
This functions send the alert to a user based on their device token.
alert - An object represnting the details of an alert  
tokens - A string, representing a unique device iidentifier.
'''
def sendToToken(request, alertID, user):
    import pyrebase


    cred = credentials.Certificate(cert_key)
    pyrebase=pyrebase.initialize_app(firebaseConfig)
    adminapp=firebase_admin.initialize_app(credential=cred)

    auth = pyrebase.auth()
    database = pyrebase.database()
    storage = pyrebase.storage()

    users = database.child("UserData").get().val()

    alertObj = AmberAlert.objects.get(id=1)
    alert = AlertSerializer(alertObj)
    test = users['ANRBGZBX6zPqwk8KOlS8Hm6bSFy1']
    tokens = list(test['tokens'])[1]

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
        'vehicle_color': alert['vehicle_model'].value,
        'vehicle_make': alert['vehicle_model'].value,
        'vehicle_LP': alert['vehicle_model'].value,
        'coords': str(alert['alert_lat'].value) + '|' + str(alert['alert_long'].value)
    },
    tokens = [tokens]
    )
    response = messaging.send_multicast(message)
    print("Sucess", response)
    return redirect('http://127.0.0.1:8000/')
