from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated # 인증된 사용자만 허용
from .models import Artist, Genre
from .utils import update_spotify_tracks_artist_genre, extract_artist, get_artist, get_top_10_tracks
import json

# @api_view(['GET', ])
# def genre_list(request):
#     if request.method == 'GET':
#         genres = Genre.objects.all()
#         serializer = GenreListSerializer(genres, many=True)
#         return Response(serializer.data)
    
@api_view(['GET', ])
def collect(request):
    if request.method == 'GET':
        data = update_spotify_tracks_artist_genre()
        return Response(data)
    
@api_view(['POST',])
def search(request):
    # 사용자의 입력 정보를 받아와서 LLM을 활용하여 가수 이름을 리스트로 추출
    user_input = request.data.get('user_input')
    response = extract_artist(user_input)
    content_str = response.choices[0].message.content

    # json 파싱
    content_dict = json.loads(content_str)

    artist_list = content_dict.get('artists', [])

    print(artist_list)

    isEmpty = False
    success = True
    tracks = []
    genres = []

    # 가수가 없으면 검색을 다시 해야함
    if not artist_list:
        isEmpty = True
        success = False

    # 가수가 여러 명이면 검색을 다시 해야함
    elif len(artist_list) > 1:
        success = False

    # 가수가 한 명이면 검색을 해야함
    elif len(artist_list) == 1:
        artist_eng = artist_list[0]["english"]
        # db에 저장되어 있는지 확인
        artist_db = Artist.objects.filter(name=artist_eng).first()

        # db에 없다면 등록
        if not artist_db:
            new_artist_id, genres = get_artist(artist_eng)

            if not new_artist_id:
                success = False

            new_artist = Artist()
            new_artist.name = artist_eng
            new_artist.artist_id = new_artist_id
            new_artist.save()

            # 장르 등록
            if genres:
                for genre in genres:
                    # 장르가 있으면 가져오고, 없으면 생성 (get_or_create 활용)
                    genre_obj, created = Genre.objects.get_or_create(name=genre)
                    
                    # Track에 장르 할당
                    new_artist.genre.add(genre_obj) 

            artist_db = new_artist
        
        # db에 있다면
        else:
            # 장르만 가져오기
            genres = artist_db.genre.values_list('name', flat=True)
            genres = list(genres)

        # 노래를 검색
        tracks = get_top_10_tracks(artist_db.artist_id)

    data = {
        'isEmpty': isEmpty,
        'success': success,
        'artist': [name["original"] for name in artist_list] if artist_list else [],
        'genre': genres,
        'tracks': tracks
    }

    print(genres)

    return Response(data)