from django.db import models
from django.contrib.auth.models import AbstractUser
from tracks.models import Genre

# Create your models here.
class User(AbstractUser):

    nickname = models.CharField(max_length=10, blank=True)
    fav_genres = models.ManyToManyField(Genre, blank=True)