from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.decorators import api_view

@api_view(['GET'])
def testapit(request):
  routes = [
    {
      'Test':'/yikes/'
    }
  ]
  return Response(routes)