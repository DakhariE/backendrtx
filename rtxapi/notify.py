# import firebase_admin
# from firebase_admin import credentials, messaging
# cred = credentials.Certificate("key.json")
# app = firebase_admin.initialize_app(cred)

# def send_to_token():
#   message = messaging.MulticastMessage(
#     notification=messaging.Notification(
#       title = "Test_Title",
#       body = "testbody"
#     ),
#     data={
#         # 'alertID': alert['id'],
#         # 'description': alert['description'],
#         # 'date': alert['date'],
#         # 'vehicle_model': alert['vehicle_model'],
#         # 'vehicle_color': alert['vehicle_model'],
#         # 'vehicle_make': alert['vehicle_model'],
#         # 'vehicle_LP': alert['vehicle_model'],
#         # 'coords': {'lat': alert['alert_lat'], 'long': alert['alert_long']}
#     },
#     tokens = ['cPW0qy_9ScatiiUmTBJwPU:APA91bEhpZJzHLkc-Dm7CHzCHvvyfpLFxEhM7e0MfhyXMP6f2nnH1ctw5yHppXAclQrDkI-ndzpIBGMcNKu7ijl-UqUyoGS1-7EqE2_4r2ZBTVmJJCdhYa-lcwzr0j0PmiOm-Ox6XAkD']
#   ) 
#   response = messaging.send_multicast(message)
#   return response

# send_to_token()