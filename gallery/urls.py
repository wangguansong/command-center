from django.urls import path

from . import views

app_name = 'gallery'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('en/', views.IndexView.as_view(), name='index'),
    path('zh/', views.IndexView.as_view(), name='index'),
]