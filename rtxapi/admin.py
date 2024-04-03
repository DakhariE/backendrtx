from django.contrib import admin

# Register your models here.
from .models import AmberAlert,UserResults

admin.site.register(AmberAlert)
admin.site.register(UserResults)