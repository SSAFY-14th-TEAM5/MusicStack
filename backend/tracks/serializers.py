from rest_framework import serializers
from .models import Track, Artist
from django.contrib.auth import get_user_model

User = get_user_model()

# class GenreListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = ('id', 'name')

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ('favorited_by', 'artist')

class FavTrackSerializer(serializers.ModelSerializer):

    class ProfileArtistSerializer(serializers.ModelSerializer):
        class Meta:
            model = Artist
            fields = ('id', 'name')

    artist = ProfileArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = ('track_name', 'artist', 'track_image_link', 'release_date_text', 'release_year')
