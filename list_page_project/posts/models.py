from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager
from django.utils import timezone

from list_page_project.core.models import TimestampedModel


class Post(TimestampedModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        comments: Manager["Comment"]

    def __str__(self):
        return self.title

    @property
    def latest_comment(self):
        return self.comments.first()

    class Meta:
        ordering = ["-created_at"]


class Comment(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}..."

    class Meta:
        ordering = ["-created_at"]
