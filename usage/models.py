from django.db import models
from django.contrib.auth.models import User

class UserQuota(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    daily_limit = models.PositiveIntegerField(
        default=100
    )

    monthly_limit = models.PositiveIntegerField(
        default=1000
    )

    def __str__(self):
        return self.user.username
    
class SearchLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    query = models.CharField(
        max_length=255
    )

    searched_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.query