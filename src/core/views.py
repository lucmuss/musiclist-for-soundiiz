from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Home page view."""
    return render(request, "core/home.html")


def health_check(request):
    """Health check endpoint."""
    return HttpResponse("OK")
