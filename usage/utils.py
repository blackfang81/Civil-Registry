from django.utils import timezone

from .models import SearchLog


def get_usage_counts(user):

    today = timezone.now().date()
    now = timezone.now()

    daily = SearchLog.objects.filter(
        user=user,
        searched_at__date=today
    ).count()

    monthly = SearchLog.objects.filter(
        user=user,
        searched_at__year=now.year,
        searched_at__month=now.month
    ).count()

    return daily, monthly
