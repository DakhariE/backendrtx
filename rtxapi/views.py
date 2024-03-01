from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.decorators import api_view
from .serializers import AlertSerializer
from .models import AmberAlert

@api_view(['GET'])
def sendAlert(request):
  alertList = AmberAlert.objects.all()
  serializer = AlertSerializer(alertList, many=True)
  return Response(serializer.data)
