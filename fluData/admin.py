# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import signals
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, House
import logging as log

from django.db.models.signals import pre_save, post_save

admin.site.register(UserProfile)
admin.site.register(House)


def refresh_house(sender, instance, **kwargs):
    if (sender is House):
        contents = instance.get_refresh_data().values()
        strs=""
        for i in contents:
            strs+=(str(i)+"||")
        instance.all_things=strs

def add_userprofile(sender, instance, created, **kwargs):
    if (sender is User) and (created):
        try:
            pass
            # usrpro = instance.userprofile
        except:
            # UserProfile.objects.create(user=instance, name=instance.username)
            print("error")

pre_save.connect(refresh_house)
post_save.connect(add_userprofile)
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='manager.log',
                filemode='w')
