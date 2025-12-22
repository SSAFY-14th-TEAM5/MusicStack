from django.urls import path
from . import views

urlpatterns = [
    path('collect/', views.collect),
    path('search/', views.search),
]
