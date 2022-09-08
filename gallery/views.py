from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import Photo

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'image_list'

    def get_queryset(self):
        return Photo.objects.filter(hidden=False, favorite=True).order_by('-taken_at')[:5]

def index(request):
    return HttpResponse("Hello, You're viewing gallery.")
