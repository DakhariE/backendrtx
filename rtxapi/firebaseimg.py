#These imports are needed to access firebase and process the photo data.
#Firebase modules are to access the database/storage
import firebase_admin
from firebase_admin import credentials, storage
#numpy and cv2 modules are to proess the images
import numpy as np
import cv2
from keys import firebaseConfig

#These to lines are needed validate session in firebase 
cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)

#This accesses the storage bucket in firebase
bucket = storage.bucket('rtx-alert-app-b343c.appspot.com')
#This blob functoin gets a speific file, as array of bytes.
print(dir(  bucket.client ))
print(bucket.client.list_buckets)
x = bucket.client.list_buckets
# x = bucket.list_blobs(prefix='submissions/')
# print(dir(x))

# for i in x:
#     print(i)

# #Converts blob into 1-D array
# array = np.frombuffer(blob.download_as_string(), np.uint8)
# #Converts array into img
# image = cv2.imdecode(array, cv2.COLOR_BGR2BGR555)

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# cars = car_id.detectMultiScale(gray, 1.1, 1)

# for (x,y,w,h) in cars:
#     cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)

# cv2.imshow('image', image)
# cv2.waitKey(0)