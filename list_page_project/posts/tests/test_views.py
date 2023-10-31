from django.contrib.auth.models import User
from django.urls import reverse
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.test import APITestCase


class PostViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "admin", "admin@test.com", "adminpassword"
        )
        self.post = Post.objects.create(
            title="Sample Post", content="test conetent", author=self.user
        )

    def test_get_post_list(self):
        url = reverse("post-list")
        response = self.client.get(url)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "admin", "admin@test.com", "adminpassword"
        )

    def test_get_create_page(self):
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_create.html")

    def test_post_create_view(self):
        post_data = {"title": "New Post Title", "content": "New post content"}
        response = self.client.post(reverse("post_create"), post_data)
        self.assertRedirects(response, reverse("post_list"))
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, "New Post Title")
