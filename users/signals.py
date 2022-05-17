from django.db.models.signals import post_save
from django.contrib.auth.models import User # User is sender
from django.dispatch import receiver
from .models import Profile


""" CREATING A PROFILE"""
@receiver(post_save, sender=User) # when a user was saved, it creates a signal
# post_save --> this signal is received by @receiver
def create_profile(sender, instance, created, **kwargs): # these arguments are passed by post_save
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) # when a user was saved, it creates a signal
# post_save --> this signal is received by @receiver
def save_profile(sender, instance, **kwargs): # these arguments are passed by post_save
    instance.profile.save()


