from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleListSerializer(serializers.ModelSerializer):
    # 댓글 수를 카운팅하기 위한 필드
    comment_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )
    
    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'content', 'comment_count',)

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('author', )

class CommentSerializer(serializers.ModelSerializer):
    class CommentAuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'nickname')

    author = CommentAuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'article')