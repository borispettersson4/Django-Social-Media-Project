from django.db.models.signals import post_save
from django.contrib.auth.models import User
#Receiver
from django.dispatch import receiver
from .models import *

#Sends signal to DB so a new Profile is created when a new account was created
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if (created):
        Profile.objects.create(user=instance)
        ProfileSettings.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
