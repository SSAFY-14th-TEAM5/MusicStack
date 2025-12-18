from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated # 인증된 사용자만 허용
from .models import Genre
from .serializers import GenreListSerializer


@api_view(['GET', ])
def genre_list(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreListSerializer(genres, many=True)
        return Response(serializer.data)