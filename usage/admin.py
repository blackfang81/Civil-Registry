from django.contrib import admin

from .models import (
    UserQuota,
    SearchLog
)

admin.site.register(UserQuota)
admin.site.register(SearchLog)