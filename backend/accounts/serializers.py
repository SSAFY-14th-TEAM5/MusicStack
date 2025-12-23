from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from tracks.models import Track

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

    followings_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'followings_count', 'followers_count',)


class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # self.user는 super().validate(attrs) 이후에 채워집니다.
        # 응답 바디(response body)에 유저의 pk와 추가 정보를 넣습니다.
        data['user_pk'] = self.user.pk

        return data
    

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('pk', 'username', 'nickname',)