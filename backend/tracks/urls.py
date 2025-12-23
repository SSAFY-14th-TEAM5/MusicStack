from django.urls import path
from . import views

urlpatterns = [
    # path('collect/', views.collect),
    path('search/', views.search),
    path('<int:user_pk>/fav/', views.fav_get),
    path('fav/create/', views.fav_save),
]
