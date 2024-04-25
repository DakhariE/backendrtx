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

database = pyrebase.database()
storage = pyrebase.storage()

Devices = database.child("Locations").get().val()
x = list(dict(Devices))


