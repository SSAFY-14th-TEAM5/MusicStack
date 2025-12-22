# 2025/12/18
- 장고 기본 세팅 - djangorestframework, django-cors-headers, dj-rest-auth, django-allauth, user
- User field - UserID(primary key), username, password, nickname, fav_gneres
- 회원가입 시에 좋아하는 장르 선택할 수 있게 추가 (vue, frontend 영역)

# 2025/12/19
- spotify api와 musicbrainz api를 이용하여 데이터 수집 
  - musicbrainz에서 장르를 담당하는 tag가 없는 track이 다수 존재 -> 장르 구분의 어려움
  - spotify api에서 artist를 기준으로 부여하는 genre 활용
  - spotify api를 이용하여 데이터베이스에 저장하는 것 확인
  - 하지만 spotify api를 이용해도 가수를 기준으로 모든 노래의 장르가 정해진다는 단점
  - spotify의 장르 구분 또한 명확하지 않고 데이터가 없는 가수 다수 존재
  - track에서의 장르는 사용자들을 통해 추가하는 방법 도모해야 할 수도

  # 2025/12/22
  - gpt5 nano를 이용해서 사용자의 질의에서 가수 이름만 추출
  - 추출한 가수 이름을 바탕으로 spotify api에서 노래 검색
  - top 10 tracks 정보 제공