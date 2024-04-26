from django.db import models
from django.db.models.functions import Now
import datetime
# Create your models here.


class AmberAlert(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(default = Now)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)
    vehicle_make = models.CharField(max_length=50)
    vehicle_info = models.TextField()
    vehicle_LP = models.CharField(max_length=10)
    alert_lat = models.CharField(max_length=100) 
    alert_long = models.CharField(max_length=100) 
    active = models.BooleanField(default=False)
    recent_Interaction = models.CharField(max_length=100, default = False) 

    def __str__(self):
        return self.name
     
class UserResults(models.Model):
    UserID = models.CharField(max_length=100)
    result_data = models.JSONField()
    date = models.DateTimeField(default = Now())

    def __str__(self):
        return self.UserID


