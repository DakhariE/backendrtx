from rest_framework import serializers
from .models import AmberAlert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmberAlert
        fields = '__all__'
