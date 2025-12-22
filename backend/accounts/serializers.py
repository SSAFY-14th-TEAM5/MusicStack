from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from tracks.models import Track
# from tracks.models import Genre

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # 추가하고 싶은 필드 정의
    nickname = serializers.CharField(max_length=10)

    # 장르 PK(ID) 리스트를 받음
    # vue 에서 ID 숫자로 이루어진 리스트를 보내면, 시리얼라이저가 자동으로 해당 ID를 가진 Genre 객체들로 변환
    # fav_genres = serializers.PrimaryKeyRelatedField(
    #     queryset=Genre.objects.all(),
    #     many=True,
    #     required=False
    # )

    def get_cleaned_data(self):
        # 부모 클래스의 기본 데이터를 가져옴
        data = super().get_cleaned_data()
        # 추가 필드 데이터를 딕셔너리에 삽입
        data['nickname'] = self.validated_data.get('nickname', '')
        # data['fav_genres'] = self.validated_data.get('fav_genres', [])
        return data

    def save(self, request):
        # 실제 User 모델에 저장하는 로직
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname')

        # Genre ManyToMany 관계 저장
        # genres = self.validated_data.get('fav_genres')
        # if genres:
        #     user.fav_genres.set(genres)

        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class ProfileTrackSerializer(serializers.ModelSerializer):
        class Meta:
            model = Track
            fields = ('track_name', 'artist_name', 'track_image_link', 'release_date_text', 'release_year')

    followings_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)

    favorite_tracks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'followings_count', 'followers_count', 'favorite_tracks')

    def get_favorite_tracks(self, obj):
        # 정렬(-id는 최신순)과 개수 제한을 적용
        tracks = obj.favorite_tracks.all().order_by('-id')[:20]
        
        # 내부 시리얼라이저인 ProfileTrackSerializer로 직렬화하여 반환합니다.
        return self.ProfileTrackSerializer(tracks, many=True).data