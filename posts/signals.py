from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post

@receiver(post_delete,sender=Post)
def delete_post_data(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(save=False)

