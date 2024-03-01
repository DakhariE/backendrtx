import numpy as np
import cv2
import pyrebase
#Use key to access firebase
# cred = credentials.Certificate("key.json")
# app = firebase_admin.initialize_app(cred)
# bucket = storage.bucket('rtx-alert-app-b343c.appspot.com')

# print(dir(bucket))
# print(bucket.get_blob)

firebase=pyrebase.initialize_app('key.json')
storage = firebase.storage()