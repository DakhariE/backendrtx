from django.db import models
import datetime
# Create your models here.


class AmberAlert(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)
    vehicle_make = models.CharField(max_length=50)
    vehicle_info = models.TextField()
    
    class Meta:
        verbose_name = "AmberAlert"