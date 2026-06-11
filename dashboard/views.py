from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .decorators import staff_required
from usage.models import GlobalQuota, UserQuota
from usage.utils import get_usage_counts


@staff_required
def home_view(request):

    return render(request, "dashboard/home.html")


@staff_required
def users_view(request):

    users = User.objects.all().order_by("username")
    rows = []

    for user in users:
        quota, _ = UserQuota.objects.get_or_create(user=user)
        daily, monthly = get_usage_counts(user)
        rows.append({
            "user": user,
            "quota": quota,
            "daily": daily,
            "monthly": monthly,
        })

    return render(request, "dashboard/users.html", {"rows": rows})


@staff_required
def edit_user_quota_view(request, user_id):

    user = get_object_or_404(User, pk=user_id)
    quota, _ = UserQuota.objects.get_or_create(user=user)
    daily, monthly = get_usage_counts(user)

    if request.method == "POST":
        quota.daily_limit = int(request.POST.get("daily_limit", quota.daily_limit))
        quota.monthly_limit = int(request.POST.get("monthly_limit", quota.monthly_limit))
        quota.save()
        return redirect("dashboard_users")

    return render(request, "dashboard/edit_user_quota.html", {
        "target_user": user,
        "quota": quota,
        "daily": daily,
        "monthly": monthly,
    })


@staff_required
def global_quota_view(request):

    global_quota = GlobalQuota.get()

    if request.method == "POST":
        global_quota.daily_limit = int(request.POST.get("daily_limit", global_quota.daily_limit))
        global_quota.monthly_limit = int(request.POST.get("monthly_limit", global_quota.monthly_limit))
        global_quota.save()

        if request.POST.get("apply_all"):
            UserQuota.objects.update(
                daily_limit=global_quota.daily_limit,
                monthly_limit=global_quota.monthly_limit,
            )

        return redirect("dashboard_home")

    return render(request, "dashboard/global_quota.html", {
        "global_quota": global_quota,
    })
