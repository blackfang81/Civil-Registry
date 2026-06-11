from django.urls import path
from .views import home_view, users_view, edit_user_quota_view, global_quota_view

urlpatterns = [
    path("", home_view, name="dashboard_home"),
    path("users/", users_view, name="dashboard_users"),
    path("users/<int:user_id>/quota/", edit_user_quota_view, name="dashboard_edit_quota"),
    path("global-quota/", global_quota_view, name="dashboard_global_quota"),
]
