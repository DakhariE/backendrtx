# import pyrebase
# import keys
# import firebase_admin
# from firebase_admin import credentials, messaging

# cred = credentials.Certificate("key.json")
# app = firebase_admin.initialize_app(cred)
# firebase=pyrebase.initialize_app(keys.firebaseConfig)

# auth = firebase.auth()
# database = firebase.database()
# storage = firebase.storage()


# users = database.child("UserData").get().val()

# def getUserData(userName):
#     return users['testuser']

# def updateUserData(userName=None, location=None, score=None, URL=None):
#     return 200

# def send_to_token(alert, tokens):
#   message = messaging.MulticastMessage(
#     notification=messaging.Notification(
#     title = alert['name'],
#     body = "Silver alert Issued to X region."
#     ),
#     data={
#         'alertID': alert['id'],
#         'description': alert['description'],
#         'date': alert['date'],
#         'vehicle_model': alert['vehicle_model'],
#         'vehicle_color': alert['vehicle_model'],
#         'vehicle_make': alert['vehicle_model'],
#         'vehicle_LP': alert['vehicle_model'],
#         'coords': {'lat': alert['alert_lat'], 'long': alert['alert_long']}
#     },
#     tokens = [tokens]
#   )
#   response = messaging.send_multicast(message)
#   return response


