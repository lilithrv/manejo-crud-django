from django.contrib import admin
from .models import User, Property, UserType, HouseType

# Register your models here.
admin.site.register(User)
admin.site.register(Property)