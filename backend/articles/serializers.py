from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'content', )

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