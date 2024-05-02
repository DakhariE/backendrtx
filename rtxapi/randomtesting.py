from django.shortcuts import render, redirect
from django.db.models.signals import post_save
import math as m
import pyrebase
from keys import *
import firebase_admin
from firebase_admin import credentials
import requests
import os
from datetime import datetime
cred = credentials.Certificate(cert_key)
pyrebase=pyrebase.initialize_app(firebaseConfig)
import random
import time

database = pyrebase.database()
storage = pyrebase.storage()

x = 'https://firebasestorage.googleapis.com/v0/b/rtx-alert-app-b343c.appspot.com/o/submissions%2Fmadza.jpg?alt=media&token=d0c0e89a-084f-4abd-8a3d-86f642488514'
y = 'https://firebasestorage.googleapis.com/v0/b/rtx-alert-app-b343c.appspot.com/o/submissions%2Fchallenger.jpg?alt=media&token=5bed6571-78cc-4434-8511-3ef591a62010'
z = 'https://firebasestorage.googleapis.com/v0/b/rtx-alert-app-b343c.appspot.com/o/submissions%2Fjeep.jpg?alt=media&token=e006d782-83eb-4fde-8fde-85062a905c67'
list = [x,y,z]

for i in range(2):
    userdata = database.child("UserData/usercon")
    x = f"sub{i}"
    userdata.update({f"{x}":{'photo':random.choice(list)}})

