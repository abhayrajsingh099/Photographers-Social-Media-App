from django.db.models.signals import post_save,pre_save,post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender , instance, **kwargs):
    instance.profile.save()   

@receiver(pre_save,sender=Profile)
def delete_old_profile_pic(sender,instance,**kwargs):
    if not instance.pk: #new profile
        return
    
    old_profile = Profile.objects.get(pk=instance.pk)

    if old_profile.photo and old_profile.photo != instance.photo:
        old_profile.photo.delete(save=False)

@receiver(post_delete,sender=Profile)
def delete_profile_data(sender, instance,**kwargs):
    if instance.photo:
        instance.photo.delete(save=False)
