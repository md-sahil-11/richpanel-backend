from django.contrib import admin
from .models import Plan, Device

admin.site.register([Plan, Device])
