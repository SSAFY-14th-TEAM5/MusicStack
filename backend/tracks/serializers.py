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


class LatestFavTrackSerializer(serializers.ModelSerializer):
    class ArtistSerializer(serializers.ModelSerializer):
        class Meta:
            model = Artist 
            fields = ['artist_id', 'name'] 

    artist = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'


class FavTrackSaveSerializer(serializers.ModelSerializer):
    # 모델에 없지만 프론트에서 보내주는 데이터를 받기 위한 필드 추가
    artist_id = serializers.ListField(
        child=serializers.CharField(), 
        required=False, 
        write_only=True
    )

    class Meta:
        model = Track
        fields = [
            'track_name', 'track_id', 'track_image_link', 
            'release_date_text', 'release_year', 'artist_id'
        ]