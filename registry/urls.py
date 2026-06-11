from django.urls import path
from django.views.generic import RedirectView

from .views import search_view

urlpatterns = [
    path("", RedirectView.as_view(url="/search/", permanent=False)),
    path("search/", search_view, name="search"),
]