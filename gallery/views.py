from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
import django_filters

from .models import Photo

# Create your views here.

class PhotoFilter(django_filters.FilterSet):
    class Meta:
        model = Photo
        fields = ['location']

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'image_list'

    def get_queryset(self):
        return Photo.objects.filter(hidden=False, favorite=True).order_by('-taken_at')[:5]

def FilterView(request):
    f = PhotoFilter(request.GET, queryset=Photo.objects.all())
    return render(request, 'gallery/test.html', {'filter': f})

def index(request):
    return HttpResponse("Hello, You're viewing gallery.")
