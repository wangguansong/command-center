from django.urls import path
from django_filters.views import FilterView
from .models import Photo
from . import views

app_name = 'gallery'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('test/', views.FilterView, name='filter_view'),
    path('en/', views.IndexView.as_view(), name='index'),
    path('zh/', views.IndexView.as_view(), name='index'),
]