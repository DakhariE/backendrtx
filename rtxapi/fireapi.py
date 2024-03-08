import numpy as np
import cv2
import pyrebase
from keys import firebaseConfig
#Use key to access firebase
# cred = credentials.Certificate("key.json")
# app = firebase_admin.initialize_app(cred)
# bucket = storage.bucket('rtx-alert-app-b343c.appspot.com')

# print(dir(bucket))
# print(bucket.get_blob)

firebase=pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#storage.child('/submissions/kobechua14@gmail.com/2024-03-01 10:49:45.831501/metadata.json').download(path='rtxapi',filename="meta.json")
file = storage.child().bucket.list_blobs()
# submissions = storage.bucket.list_blobs('submissions/')
print(file)
for x in file:
    print(x)