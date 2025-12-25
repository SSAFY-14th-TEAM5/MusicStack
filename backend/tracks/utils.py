import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import musicbrainzngs as mb
import json
from .models import Track, Artist
from dotenv import load_dotenv
import os
import time
from pprint import pprint
import random
from openai import OpenAI
import requests

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 요청 헤더에 한국어를 1순위로 설정
sp._session.headers.update({
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
})

client = OpenAI(
    api_key = os.getenv("GMS_KEY"),
    base_url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"
)


def extract_artist(user_input):

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "developer",
                "content": """
                너는 Spotify API 검색을 위한 '아티스트 이름 추출' 도우미야.

                입력 문장에서 아티스트(가수/그룹/밴드) 이름만 찾아서 반환해.
                아티스트 이름을 번역/로마자 변환/추론해서 바꾸지 말고, 입력에 등장한 표기를 최대한 그대로 유지해.

                [추출 규칙]
                1) 입력에 아티스트 이름이 한국어로 등장하면, '한국어 표기 그대로' 반환한다.
                - 예: "블랙핑크 노래 추천해줘" -> "블랙핑크"
                - 예: "아이유랑 뉴진스" -> "아이유", "뉴진스"
                2) 입력에 아티스트 이름이 영어/라틴 문자로 등장하면, 철자 수정 없이 그대로 반환한다.
                - 예: "Taylor Swift top10" -> "Taylor Swift"
                - 예: "coldplay" -> "coldplay" (수정 금지)
                3) 아티스트가 확실하지 않으면 포함하지 않는다.
                4) 입력에 아티스트가 없으면 빈 배열을 반환한다.
                5) 임의로 새로운 아티스트명을 생성하거나 추측하지 않는다.

                [출력 형식 제약]
                - 반드시 JSON 단일 객체만 출력한다.
                - 설명/주석/마크다운/추가 텍스트를 절대 포함하지 않는다.
                - 결과 형식은 아래와 정확히 일치해야 한다.

                {
                "artists": [
                    {
                    "original": "원본에서 추출한 아티스트명",
                    "query": "Spotify 검색에 사용할 문자열(원본 표기 그대로)"
                    }
                ]
                }

                [예시]
                입력: "정승환"
                출력: {"artists":[{"original":"정승환","query":"정승환"}]}

                입력: "블랙핑크 노래 추천해줘"
                출력: {"artists":[{"original":"블랙핑크","query":"블랙핑크"}]}

                입력: "아이유랑 뉴진스 알려줘"
                출력: {"artists":[{"original":"아이유","query":"아이유"},{"original":"뉴진스","query":"뉴진스"}]}

                입력: "Taylor Swift 추천"
                출력: {"artists":[{"original":"Taylor Swift","query":"Taylor Swift"}]}

                입력: "점심 메뉴 추천해줘"
                출력: {"artists":[]}
                """
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response


def get_artist(artist_name):
    results = sp.search(q=artist_name, type='artist', limit=1, market='KR')
    items = results['artists']['items']
    
    if len(items) > 0:
        artist = items[0]
        return artist['id'], artist['genres'], artist['name']
    
    return None, [], None


def get_top_10_tracks(artist_id):
    results = sp.artist_top_tracks(artist_id, country='KR')
    top_tracks = []
    for track in results['tracks']:
        top_tracks.append({
            'track_name': track['name'],
            'artist_name': track['artists'][0]['name'],
            'artist_id': [artist['id'] for artist in track['artists']],
            'track_id': track['id'],
            'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'release_date': track['album']['release_date'],
            'release_year': int(track['album']['release_date'][:4])
        })
        
    return top_tracks


def get_video_id(query):
    api_key = os.getenv("YOUTUBE_API_KEY")
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': api_key,
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 1
    }
    response = requests.get(url, params=params).json()

    try:
        return response['items'][0]['id']['videoId']
    except (IndexError, KeyError):
        return None


def recommend_music(fav_musics):
    payload = {"liked_tracks": fav_musics}

    response = client.chat.completions.create(
        model="gpt-5.2",
        temperature=0.3,
        messages=[
            {
                "role": "developer",
                "content": """
                    liked_tracks는 아래 형식의 배열이다:
                    [
                        {"track":"곡명","artist":"아티스트","genres":["..."] (선택)}
                    ]

                    너는 음악 추천 시스템이다.
                    입력된 liked_tracks의 분위기/장르/아티스트 성향을 요약하고, 비슷한 곡을 5개 추천해라.

                    규칙:
                    - 좋아하는 곡 목록을 기반으로 추천해라.
                    - 존재하지 않는 곡/아티스트를 만들어내지 마라.
                    - 결과는 반드시 JSON만 출력한다(설명/마크다운 금지).
                    - 추천은 (track, artist) 형태로만 제시한다.
                    - liked_tracks에 있는 곡은 추천 목록에서 제외한다.
                    - reason은 20자 이내로 작성한다.

                    출력 형식:
                    {
                    "taste_summary": "한 문장 요약",
                    "recommended": [
                        {"track": "곡명", "artist": "아티스트", "reason": "짧은 이유"}
                    ]
                    }
                """
            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False)
            }
        ]
    )

    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except:
        return {"taste_summary": "", "recommended": []}




# def update_spotify_tracks_artist_genre():
#     # JSON 형식의 API를 반복을 통해 리스트에 담고, 각 리스트에 담긴 데이터를 JSON 파일로 저장하는 과정입니다.
#     track_data = []
#     return_data = []

#     for i in range(0, 100, 50):
#         # 연도를 기준으로 검색
#         # track_results = sp.search(q='year:2025', type='track', limit=50, offset=i)

#         # 랜덤하게 트랙 수집
#         random_char = random.choice('abcdefghijklmnopqrstuvwxyz')
#         query = f"%{random_char}%"
        
#         # 2. 랜덤한 시작 위치(offset) 설정, Spotify 검색 결과는 최대 10,000개까지 접근 가능
#         random_offset = random.randint(0, 500) 
        
#         # 3. 검색 실행
#         track_results = sp.search(q=query, type='track', limit=10, offset=random_offset)

#         for t in track_results['tracks']['items']:

#             if Track.objects.filter(track_id=t['id']).exists():
#                 continue

#             # 아티스트 정보를 통해 장르 정보 가져오기
#             artist_id = t['artists'][0]['id']
#             artist_info = sp.artist(artist_id)  # 아티스트 정보 가져오기
#             genres = artist_info['genres']  # 장르 정보 가져오기

#             track_db = Track()
#             track_db.track_name = t['name']
#             track_db.track_id = t['id']
#             track_db.track_popularity = t['popularity']
#             track_db.artist_name = t['artists'][0]['name']
#             track_db.release_date_text = t['album']['release_date']
#             track_db.release_year = int(t['album']['release_date'][:4])
#             track_db.duration_ms = t['duration_ms']
#             track_db.track_image_link = t['album']['images'][0]['url']
#             track_db.save() # 장르 추가 전에 먼저 저장

#             print(track_db.track_name)
#             print(genres)

#             # 아티스트 정보가 이미 있다면 건너뜀
#             if Artist.objects.filter(artist_id=artist_id).exists():
#                 artist_obj = Artist.objects.get(artist_id=artist_id)
#                 track_db.artist.add(artist_obj)
#                 continue

#             # 아티스트 정보가 없다면 아티스트 객체를 저장
#             artist_db = Artist()
#             artist_db.name = t['artists'][0]['name']
#             artist_db.artist_id = artist_id

#             # 저장 후 장르 정보 추가
#             artist_db.save()

#             if genres:
#                 for genre in genres:
#                     # 장르가 있으면 가져오고, 없으면 생성 (get_or_create 활용)
#                     genre_obj, created = Genre.objects.get_or_create(name=genre)
                    
#                     # Track에 장르 할당
#                     # 만약 ForeignKey라면 한 트랙에 장르 하나만 저장됨 (마지막 것이 덮어씀)
#                     artist_db.genre.add(genre_obj) 

#             # 예시: 스포티파이에서 가져온 트랙 정보
#             track_name = track_db.track_name
#             artist_name = track_db.artist_name

#             return_data = {
#                 'status': 'saved',
#                 'name': track_db.track_name,
#                 'artist': track_db.artist_name,
#                 'spotify_id': track_db.track_id,
#                 'genre': genres,
#             }
            
#             # API 부하를 줄이기 위해 짧은 휴식 (권장)
#             time.sleep(1)
    
#     return return_data



# def collect_pop_tracks():
#     # 1. 'pop' 장르를 가진 아티스트들을 검색 (시장을 'US'로 설정하여 국내곡 제외)
#     results = sp.search(q='genre:pop', type='artist', limit=50, market='US')
    
#     for artist in results['artists']['items']:
#         artist_name = artist['name']
#         genres = artist['genres'] 
#         artist_id = artist['id']

#         # 아티스트가 있으면 가져오고, 없으면 생성 (get_or_create 활용)
#         artist_obj, created = Artist.objects.get_or_create(artist_id=artist_id)
        
#         # 새로운 아티스트면 장르 추가
#         if created:
#             artist_obj.name = artist_name
#             artist_obj.artist_id = artist_id
#             artist_obj.save()

#             for genre in genres:
#                 genre_obj, created = Genre.objects.get_or_create(name=genre)
#                 artist_obj.genre.add(genre_obj)
        
#         # 2. 해당 아티스트의 인기 곡(Top Tracks) 가져오기
#         top_tracks = sp.artist_top_tracks(artist_id, country='US')['tracks']

#         print(top_tracks)
        
#         for t in top_tracks:
#             track_name = t['name']
            
#             # (중복 체크 로직)
#             if Track.objects.filter(track_id=t['id']).exists():
#                 print("이미 존재함")
#                 continue

#             # (저장 로직)
#             track_db = Track()
#             track_db.track_name = t['name']
#             track_db.track_id = t['id']
#             track_db.track_popularity = t['popularity']
#             track_db.artist_name = t['artists'][0]['name']
#             track_db.release_date_text = t['album']['release_date']
#             track_db.release_year = int(t['album']['release_date'][:4])
#             track_db.duration_ms = t['duration_ms']
#             track_db.track_image_link = t['album']['images'][0]['url']
#             track_db.save() # 장르 추가 전에 먼저 저장

#             print(track_db.track_name)
#             print(genres)
            
#             print(f"✅ 수집 완료: {artist_name} - {track_name} (장르: {genres})")


# def get_musicbrainz_recording_id(track_name, artist_name):
#     try:
#         # 트랙명과 아티스트명으로 뮤직브레인즈에서 검색
#         result = mb.search_recordings(track_name, artist=artist_name, limit=5)
        
#         # 첫 번째 검색 결과에서 recording ID 추출
#         recordings = result.get('recording-list', [])
#         if recordings:
#             return recordings[0]['id']  # 첫 번째 녹음의 ID 반환
#         else:
#             return None  # 해당 트랙이 없으면 None 반환
#     except mb.WebServiceError as e:
#         print(f"WebServiceError: {e}")
#         return None
            

# def update_spotify_tracks():
#     # JSON 형식의 API를 반복을 통해 리스트에 담고, 각 리스트에 담긴 데이터를 JSON 파일로 저장하는 과정입니다.
#     track_data = []
#     return_data = []

#     # MusicBrainz API 설정
#     mb.set_useragent("MyApp", "1.0", "your_email@example.com")  # 사용자 정보 설정
#     for i in range(0, 10, 10):
#         track_results = sp.search(q='track', type='track', limit=20, offset=i, market='US')
#         # track_results = sp.search(q='year:2025', type='track', limit=50, offset=i)
#         print(track_results)
#         for t in track_results['tracks']['items']:

#             if Track.objects.filter(track_id=t['id']).exists():
#                 continue

#             track_db = Track()
#             track_db.track_name = t['name']
#             track_db.track_id = t['id']
#             track_db.track_popularity = t['popularity']
#             track_db.artist_name = t['artists'][0]['name']
#             track_db.artist_id = t['artists'][0]['id']
#             track_db.release_date_text = t['album']['release_date']
#             track_db.release_year = int(t['album']['release_date'][:4])
#             track_db.duration_ms = t['duration_ms']
#             track_db.track_image_link = t['album']['images'][0]['url']
#             track_db.save() # 장르 추가 전에 먼저 저장

#             pprint(track_db.track_name)

#             # 예시: 스포티파이에서 가져온 트랙 정보
#             track_name = track_db.track_name
#             artist_name = track_db.artist_name

#             # 뮤직브레인즈에서 트랙 ID 찾기
#             mbid = get_musicbrainz_recording_id(track_name, artist_name)

#             print(mbid)

#             # 획득한 Recording ID를 변수에 저장합니다. (예: Dua Lipa의 Blow Your Mind (Mwah))
#             recording_id = mbid

#             if not mbid: # 👈 추가: ID를 못 찾으면 다음 곡으로 넘어감
#                 print(f"⏩ {track_name}에 대한 MusicBrainz ID를 찾을 수 없습니다.")
#                 continue

#             try:
#                 # 💥 get_recording_by_id 함수를 사용하고 includes=['tags']를 명시합니다.
#                 result = mb.get_recording_by_id(
#                     recording_id, 
#                     includes=['tags']  
#                 )

#                 print(result)
                
#                 # 결과에서 'recording' 키 아래의 'tag-list'를 추출합니다.
#                 tags = result['recording'].get('tag-list', [])
                
#                 if tags:
#                     tags_tuple_list = []
#                     for tag in tags:
#                         # 태그 투표 수, 태그 이름 쌍을 튜플로 저장
#                         tags_tuple_list.append((tag['count'], tag['name']))
#                     # 투표 수를 기준으로 내림차순으로 정렬
#                     tags_tuple_list.sort(reverse=True)

#                     # 상위 3개만 반복
#                     for count, genre_name in tags_tuple_list[:3]:
#                         # 장르가 있으면 가져오고, 없으면 생성 (get_or_create 활용)
#                         genre_obj, created = Genre.objects.get_or_create(name=genre_name)
                        
#                         # Track에 장르 할당 (Many-to-Many 관계일 경우 .add() 사용)
#                         # 만약 ForeignKey라면 한 트랙에 장르 하나만 저장됨 (마지막 것이 덮어씀)
#                         track_db.genre.add(genre_obj) 
                        
#                 else:
#                     track_db.save() # 태그 없어도 기본 정보는 저장
#                     print(f"❌ Recording ID: {recording_id}에는 현재 부여된 태그가 없습니다.")

#             except mb.WebServiceError as exc:
#                 print(f"MusicBrainz API 오류 발생: {exc}")

#             return_data = {
#                 'status': 'saved',
#                 'name': track_db.track_name,
#                 'artist': track_db.artist_name,
#                 'spotify_id': track_db.track_id,
#             }
            
#             # API 부하를 줄이기 위해 짧은 휴식 (권장)
#             time.sleep(1)
    
#     return return_data
