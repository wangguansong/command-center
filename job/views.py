from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

#@login_required
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse("Hello, world. You're not logged in.")
    else:
        return HttpResponse("Hello, world. You're logged in.")
