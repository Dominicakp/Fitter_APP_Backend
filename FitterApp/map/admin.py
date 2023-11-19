from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin

@admin.register(User)
class UserAdmin(OSMGeoAdmin):
    list_display = ('username', 'location', 'user_type')
