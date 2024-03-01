from django.db import models
import datetime
# Create your models here.


class AmberAlert(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)
    vehicle_make = models.CharField(max_length=50)
    vehicle_info = models.TextField()
    vehicle_LP = models.CharField(max_length=10)
    alert_lat = models.CharField(max_length=10,default = "28.0587 N") 
    alert_long = models.CharField(max_length=10,default = "82.4139 W") 
    class Meta:
        verbose_name = "AmberAlert"
