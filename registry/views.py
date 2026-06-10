from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

from datetime import timedelta
import time

from .models import Citizen
from usage.models import SearchLog, UserQuota


@login_required
def search_view(request):

    q = request.GET.get("q")

    if not q:
        return render(
            request,
            "registry/search.html"
        )

    if len(q) < 3:
        return render(
            request,
            "registry/search.html",
            {
                "error": "حداقل 3 کاراکتر وارد کنید"
            }
        )

    quota = UserQuota.objects.get(
        user=request.user
    )

    # مصرف روزانه
    today = timezone.now() - timedelta(days=1)

    daily_count = SearchLog.objects.filter(
        user=request.user,
        searched_at__gte=today
    ).count()

    # مصرف ماهانه
    now = timezone.now()

    monthly_count = SearchLog.objects.filter(
        user=request.user,
        searched_at__year=now.year,
        searched_at__month=now.month
    ).count()

    if daily_count >= quota.daily_limit:
        return render(
            request,
            "registry/search.html",
            {
                "error": "سقف مصرف روزانه تکمیل شده"
            }
        )

    if monthly_count >= quota.monthly_limit:
        return render(
            request,
            "registry/search.html",
            {
                "error": "سقف مصرف ماهانه تکمیل شده"
            }
        )

    start = time.perf_counter()

    queryset = Citizen.objects.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(national_code__icontains=q) |
        Q(phone_number__icontains=q)
    )

    result_count = queryset.count()

    results = queryset[:100]

    elapsed_time = time.perf_counter() - start

    SearchLog.objects.create(
        user=request.user,
        query=q
    )

    context = {
        "results": results,
        "count": result_count,
        "elapsed_time": round(elapsed_time, 4),
    }

    return render(
        request,
        "registry/search.html",
        context
    )