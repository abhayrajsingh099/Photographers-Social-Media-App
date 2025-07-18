from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Delete users who haven't logged in for 5+ mins"

    def handle(self,*args, **kwargs):
        threshold_date = timezone.now() - timedelta(minutes=5)
        inactive_users = User.objects.filter(last_login__lt=threshold_date)
        count = inactive_users.count()
        inactive_users.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} inactive users. "))