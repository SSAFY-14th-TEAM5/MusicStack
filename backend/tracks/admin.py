from django.contrib import admin
from .models import Track, Genre, Artist, Playlist

# Register your models here.
admin.site.register(Track)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Playlist)