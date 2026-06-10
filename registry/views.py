from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def search_view(request):

    return render(
        request,
        "registry/search.html"
    )