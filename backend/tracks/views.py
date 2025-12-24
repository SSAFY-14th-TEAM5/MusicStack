from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated # 인증된 사용자만 허용
from .models import Artist, Genre, Track
from .utils import extract_artist, get_artist, get_top_10_tracks, get_video_id
import json
from .serializers import TrackSerializer, FavTrackSerializer, LatestFavTrackSerializer, FavTrackSaveSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

# @api_view(['GET', ])
# def genre_list(request):
#     if request.method == 'GET':
#         genres = Genre.objects.all()
#         serializer = GenreListSerializer(genres, many=True)
#         return Response(serializer.data)
    
# @api_view(['GET', ])
# def collect(request):
#     if request.method == 'GET':
#         data = update_spotify_tracks_artist_genre()
#         return Response(data)
    
@api_view(['POST',])
def search(request):
    # 사용자의 입력 정보를 받아와서 LLM을 활용하여 가수 이름을 리스트로 추출
    user_input = request.data.get('user_input')
    response = extract_artist(user_input)
    content_str = response.choices[0].message.content

    # json 파싱
    content_dict = json.loads(content_str)

    artist_list = content_dict.get('artists', [])

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

        # 반환된 결과를 통해 유튜브 video id 검색 
        for track in tracks:
            # 1. DB에서 해당 트랙을 먼저 찾음
            track_obj = Track.objects.filter(track_id=track["track_id"]).first()

            # 2. DB에 있고 video_id도 있다면 바로 사용
            if track_obj and track_obj.video_id:
                track["video_id"] = track_obj.video_id
                

            else:
            # 3. DB에 없거나 video_id가 없다면 유튜브 검색 실행
                search_query = f"{track['artist_name']} {track['track_name']} official mv"
                video_id = get_video_id(search_query)
                track["video_id"] = video_id # 찾았으면 id, 못 찾았으면 None
                
                # 4. 검색 결과를 DB에 반영 (저장)
                if video_id:
                    if track_obj:
                        # DB에 트랙은 있는데 video_id만 없었던 경우
                        track_obj.video_id = video_id
                        track_obj.save()
                        track_obj.artist.add(artist_db)
                    else:
                        # DB에 트랙 자체가 없었던 경우 (필요 시 새로운 객체 생성)
                        # Track.objects.create(track_id=track["track_id"], video_id=video_id, ...)
                        new_track = Track.objects.create(
                            track_id=track["track_id"],
                            track_name=track["track_name"],
                            video_id=video_id,
                            track_image_link=track.get("album_image", ""), # 프론트에서 쓰는 필드들 저장
                            release_date_text=track["release_date"],
                            release_year=track["release_year"],
                        )
                        new_track.artist.add(artist_db)

    data = {
        'isEmpty': isEmpty,
        'success': success,
        'artist': [name["original"] for name in artist_list] if artist_list else [],
        'genre': genres,
        'tracks': tracks
    }

    return Response(data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def fav_save(request):
    track_data = request.data.get('track')

    if not track_data:
        return Response({"error": "데이터가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 시리얼라이저에 데이터를 넣고 검증
    serializer = FavTrackSaveSerializer(data=track_data)

    if serializer.is_valid():

        # 중요: request.data가 아닌 serializer.validated_data를 사용하세요!
        v_data = serializer.validated_data
        artist_ids = v_data.get('artist_id') # 이제 여기서 데이터가 나옵니다.
        
        # 트랙 생성/조회
        track, created = Track.objects.get_or_create(
            track_id=v_data.get('track_id'),
            defaults={
                'track_name': v_data.get('track_name'),
                'release_date_text': v_data.get('release_date_text'),
                'release_year': v_data.get('release_year'),
                'track_image_link': v_data.get('track_image_link'),
            }
        )

        # 아티스트 연결 로직
        if artist_ids:
            for aid in artist_ids:
                artist, _ = Artist.objects.get_or_create(artist_id=aid.strip())
                track.artist.add(artist)

        # 3. 좋아요 추가
        track.favorited_by.add(request.user)
        
        return Response({"message": "좋아요"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def fav_get(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    tracks = user.favorite_tracks.all().order_by('-id')

    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(tracks, request)

    if page is not None:
        # 시리얼라이즈 (전체 tracks가 아닌 쪼개진 page 데이터를 넣음)
        serializer = FavTrackSerializer(page, many=True)
        # 페이지네이션 전용 응답 반환 (count, next, previous 등이 포함됨)
        return paginator.get_paginated_response(serializer.data)

    # 페이지 데이터가 없는 경우의 기본 응답
    serializer = FavTrackSerializer(tracks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def fav_latest(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    latest_track = user.favorite_tracks.order_by('-id').prefetch_related('artist').first()

    if not latest_track:
        return Response({"message": "좋아요한 트랙이 없습니다."}, status=404)
    
    # 유튜브 id가 db에 없다면 검색
    if not latest_track.video_id:
        # 유튜브 검색어 생성
        artist_name = " ".join(latest_track.artist.all().values_list('name', flat=True))
        search_query = f"{artist_name} {latest_track.track_name} official mv"
    
        video_id = get_video_id(search_query)

        if video_id:
            latest_track.video_id = video_id
            latest_track.save()

        else:
            return Response({"message": "비디오를 찾을 수 없습니다."}, status=404)
    
    serializer = LatestFavTrackSerializer(latest_track)
    return Response(serializer.data, status=200)

    
