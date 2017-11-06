# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import signals
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Person, tHouse, UserProfile, House

# class UserInline(admin.StackedInline):
#     model = Person
#     can_delete = False
#     verbose_name_plural = "user"

def syncToUsers(sender, **kwargs):
    # print(kwargs)
    # if kwargs
    pass

signals.post_save.connect(syncToUsers)


admin.site.register(Person)
admin.site.register(tHouse)
admin.site.register(UserProfile)
admin.site.register(House)