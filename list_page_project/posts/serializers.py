from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    latest_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "author", "content", "latest_comment"]

    def get_latest_comment(self, obj: Post):
        latest_comment = obj.latest_comment
        return CommentSerializer(latest_comment).data if latest_comment else None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]
