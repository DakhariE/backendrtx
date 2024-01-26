import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2

cred = credentials.Certificate("/key.json")
app = firebase_admin.initialize_app(cred, {'storagebucket': 'rtx-alert-app.appspot.com' })

bucket = storage.bucket()

blob = bucket.get_blob("OIP[2].jpg")

arr = np.frombuffer(blob.download_as_string(), np.uint8)

img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)

cv2.imshow('image', img)
cv2.waitkey(0)

