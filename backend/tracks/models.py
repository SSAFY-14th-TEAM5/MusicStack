from django.db import models
from django.conf import settings

# Create your models here.
class Track(models.Model):
    artist = models.ManyToManyField('Artist', blank=True )
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_tracks', blank=True)
    track_name = models.TextField()
    track_id = models.TextField()
    release_date_text = models.CharField(max_length=10, null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    track_image_link = models.URLField()
    video_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.track_name

class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Artist(models.Model):
    genre = models.ManyToManyField(Genre, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_artists', blank=True)
    name = models.CharField(max_length=100)
    artist_id = models.TextField()

# class Playlist(models.Model):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
#     tracks = models.ManyToManyField('Track', related_name='playlists', blank=True)
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     is_public = models.BooleanField(default=True) # 공개 여부
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.owner.nickname}의 플레이리스트: {self.title}"