from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Comment, Post


class PostModelTest(TestCase):
    @classmethod
    def setUp(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()
        test_post = Post.objects.create(
            title="Test Post", content="test post", author=test_user
        )
        test_post.save()

    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f"{post.content}"

        self.assertEquals(expected_object_name, "test post")

    def test_post_str_representation(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEquals(str(post), expected_object_name)

    def test_lastest_comment(self):
        post = Post.objects.get(id=1)
        test_user = User.objects.get(username="testuser")
        Comment.objects.create(post=post, author=test_user, content="Test comment")
        Comment.objects.create(post=post, author=test_user, content="Test comment2")
        self.assertEquals(post.lastest_comment.content, "Test comment2")


class CommentModelTest(TestCase):
    @classmethod
    def setUp(cls):
        test_user = User.objects.create_user(username="testuser2", password="12345")
        test_post = Post.objects.create(
            title="Test Post 2", content="test post", author=test_user
        )
        Comment.objects.create(
            post=test_post, author=test_user, content="Test comment on post 2"
        )

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f"{comment.content}"
        self.assertEquals(expected_object_name, "Test comment on post 2")

    def test_comment_str_representation(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f"{comment.author.username}: {comment.content[:20]}..."
        self.assertEquals(str(comment), expected_object_name)
