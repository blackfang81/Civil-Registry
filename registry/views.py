from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import time

from .models import Citizen
from .search_utils import build_query_filter
from usage.models import SearchLog, UserQuota
from usage.utils import get_usage_counts


@login_required
def search_view(request):

    q = request.GET.get("q", "").strip()
    father_name = request.GET.get("father_name", "").strip()
    birth_from = request.GET.get("birth_from", "").strip()
    birth_to = request.GET.get("birth_to", "").strip()

    quota = UserQuota.objects.get(user=request.user)
    daily_count, monthly_count = get_usage_counts(request.user)

    context = {
        "daily_count": daily_count,
        "daily_limit": quota.daily_limit,
        "monthly_count": monthly_count,
        "monthly_limit": quota.monthly_limit,
        "father_name": father_name,
        "birth_from": birth_from,
        "birth_to": birth_to,
    }

    if not q and not father_name and not birth_from and not birth_to:
        return render(request, "registry/search.html", context)

    if q and len(q) < 3:
        context["error"] = "حداقل ۳ کاراکتر وارد کنید"
        return render(request, "registry/search.html", context)

    if daily_count >= quota.daily_limit:
        context["error"] = "سقف مصرف روزانه تکمیل شده است"
        return render(request, "registry/search.html", context)

    if monthly_count >= quota.monthly_limit:
        context["error"] = "سقف مصرف ماهانه تکمیل شده است"
        return render(request, "registry/search.html", context)

    start = time.perf_counter()

    queryset = Citizen.objects.all()

    if q:
        q_filter, error = build_query_filter(q)
        if error:
            context["error"] = error
            return render(request, "registry/search.html", context)
        queryset = queryset.filter(q_filter)

    if father_name:
        queryset = queryset.filter(father_name__icontains=father_name)

    if birth_from:
        queryset = queryset.filter(birth_date__gte=birth_from)

    if birth_to:
        queryset = queryset.filter(birth_date__lte=birth_to)

    result_count = queryset.count()
    results = list(queryset[:100])

    elapsed_time = time.perf_counter() - start

    SearchLog.objects.create(user=request.user, query=q or "فیلتر")

    context.update({
        "results": results,
        "count": result_count,
        "elapsed_time": round(elapsed_time, 4),
    })

    return render(request, "registry/search.html", context)
