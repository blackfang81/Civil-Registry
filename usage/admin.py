from django.contrib import admin

from .models import GlobalQuota, UserQuota, SearchLog

admin.site.register(GlobalQuota)
admin.site.register(UserQuota)
admin.site.register(SearchLog)
