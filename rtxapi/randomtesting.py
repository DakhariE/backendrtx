from django.shortcuts import render, redirect
from django.db.models.signals import post_save
import math as m
import pyrebase
from keys import *
import firebase_admin
from firebase_admin import credentials
import requests
import os

cred = credentials.Certificate(cert_key)
pyrebase=pyrebase.initialize_app(firebaseConfig)

database = pyrebase.database()
storage = pyrebase.storage()

# # users = database.child("UserData").get().val()
# # data = database.child("UserData/YJTCNKotRiMWHugY2a9wgBlmutu2/submissions").get().val()
# # mostRecentSub = next(reversed(data))
# # up = database.child(f"UserData/YJTCNKotRiMWHugY2a9wgBlmutu2/submissions/{mostRecentSub}").get().val()
# # print(up)

data22 = {"test": 5, "Success": False}
findingUpdateLocation = database.child(f"UserData/RT5Bfq5TaSfXsHQEUznoT82QWGe2/submissions").get().val()
mostRecentSub = next(reversed(findingUpdateLocation))
print(mostRecentSub)
# findingUpdateLocation = database.child(f"UserData/RT5Bfq5TaSfXsHQEUznoT82QWGe2/submissions").get().val()
# mostRecentSub = next(reversed(findingUpdateLocation))
# print(mostRecentSub)