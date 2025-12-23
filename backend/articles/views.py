from django.shortcuts import render
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-id')

        # 1. 페이지네이션 객체 설정
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 한 페이지당 게시글 수
        
        # 2. 쿼리셋 쪼개기
        page = paginator.paginate_queryset(articles, request)
        
        if page is not None:
            # 3. 쪼개진 데이터(page)를 시리얼라이즈
            serializer = ArticleListSerializer(page, many=True)
            # 4. 페이지네이션 정보가 포함된 응답 반환
            return paginator.get_paginated_response(serializer.data)
        
        # 페이지네이션 설정이 없을 경우를 대비한 기본 응답
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'DELETE', 'PATCH'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if article.author != request.user:  
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PATCH':
        if article.author != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET', 'POST', ])
def comment_list(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        comments = article.comments.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(comments, request)
        
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 중요: 어떤 게시글의 댓글인지 저장할 때 명시해줘야 함
            serializer.save(article=article, author=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, article_pk, comment_pk):
    article = Article.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if comment.author != request.user:  
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        if comment.author != request.user:  
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
