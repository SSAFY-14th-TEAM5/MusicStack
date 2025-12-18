from django.db import models
from django.conf import settings

# Create your models here.
class Track(models.Model):
    genre = models.ManyToManyField('Genre', blank=True)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_tracks', blank=True)
    track_name = models.TextField()
    track_id = models.TextField()
    track_popularity = models.IntegerField()
    artist_name = models.TextField()
    artist_id = models.TextField()
    release_year = models.DateField()
    duration_ms = models.IntegerField()
    track_image_link = models.URLField()

    def set_default_genre(self):
        # Track이 생성될 때 기본 장르를 할당
        default_genre = Genre.objects.get(name="Undefined")  # Undefined를 기본으로
        self.genreId.add(default_genre)

class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Artist(models.Model):
    genre = models.ManyToManyField(Genre, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_artists', blank=True)
    name = models.CharField(max_length=100)

class Playlist(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField('Track', related_name='playlists', blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True) # 공개 여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.nickname}의 플레이리스트: {self.title}"