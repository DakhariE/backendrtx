from rest_framework import serializers
from .models import AmberAlert, UserResults

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmberAlert
        fields = '__all__'

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResults
        fields = '__all__' 