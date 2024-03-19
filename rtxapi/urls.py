from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.sendAlert),
    path("sendal/<str:alertID>/<str:user>",views.sendToToken)
]