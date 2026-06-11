from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from usage.models import GlobalQuota, UserQuota


@receiver(post_save, sender=User)
def create_quota(sender, instance, created, **kwargs):

    if created:
        global_quota = GlobalQuota.get()
        UserQuota.objects.create(
            user=instance,
            daily_limit=global_quota.daily_limit,
            monthly_limit=global_quota.monthly_limit,
        )
