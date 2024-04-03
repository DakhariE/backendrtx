'''
This files defines the urls to call a specific funtion.
    Example. 
        "sendal/<str:alertID>/<str:user>",views.sendToToken
        sendal/ Is the url for sending alerts, The string "sendal" is arbitrary.
        /<str:alertID>/, takes a str as the next url argument and puts it into the function sendToToken located in the views file
        /<str:user>, does the same as above
        views is the file containing logic functions
        sendToToken is a function in the view file.
This file is an extention of the original url.py located in backendrtx which is the root of the backend application.
'''

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.sendAlert),
]   