# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import signals
from django.contrib import admin
from django.contrib.auth.models import User

from .models import UserProfile, House

admin.site.register(UserProfile)
admin.site.register(House)