from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from usage.models import UserQuota

@receiver(post_save, sender=User)
def create_quota(sender, instance, created, **kwargs):

    if created:
        UserQuota.objects.create(
            user=instance
        )