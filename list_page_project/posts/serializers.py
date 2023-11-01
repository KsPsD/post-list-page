from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    latest_comment = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author", "content", "latest_comment"]

    def get_latest_comment(self, obj):
        if hasattr(obj, "latest_comment_prefetched") and obj.latest_comment_prefetched:
            return CommentSerializer(obj.latest_comment_prefetched[0]).data
        return None
