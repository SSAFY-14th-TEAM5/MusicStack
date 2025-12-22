from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

User = get_user_model()
# Create your views here.
@api_view(['GET', ])
def profile(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(
            User.objects.annotate(
                followings_count=Count('followings'),
                followers_count=Count('followers')
            ),
            pk=user_id
        )

        serializer = ProfileSerializer(user)
        return Response(serializer.data)