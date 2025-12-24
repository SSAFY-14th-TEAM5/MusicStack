from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

User = get_user_model()
# Create your views here.
@api_view(['GET', ])
def profile(request, user_pk):
    if request.method == 'GET':
        user_queryset = User.objects.annotate(
            followings_count=Count('followings'),
            followers_count=Count('followers')
        ).prefetch_related('favorite_tracks')

        # 2. 미리 준비한 쿼리셋에서 특정 유저를 찾습니다.
        user = get_object_or_404(user_queryset, pk=user_pk)

        serializer = ProfileSerializer(user)
        return Response(serializer.data)
