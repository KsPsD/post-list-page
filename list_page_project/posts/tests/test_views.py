from django.contrib.auth.models import User
from django.urls import reverse
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.test import APITestCase


class PostViewSetTestCase(APITestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_superuser("admin", "admin@test.com", "adminpassword")
        Post.objects.create(title="Sample Post", content="test conetent", author=user)
        Post.objects.create(
            title="Sample Post 2", content="test conetent 2", author=user
        )
        Post.objects.create(
            title="Sample Post 3", content="test conetent 3", author=user
        )

    def test_get_post_list(self):
        url = reverse("post-list")
        response = self.client.get(url)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_post(self):
        search_term = "Sample"
        url = reverse("post-list") + f"?search={search_term}"
        response = self.client.get(url)

        # 검색 결과를 기대하는 포스트만 필터링
        filtered_posts = Post.objects.filter(title__icontains=search_term)
        serializer = PostSerializer(filtered_posts, many=True)

        # 검색 결과가 serializer를 통해 반환된 데이터와 일치하는지 확인
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostCreateViewTestCase(APITestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser("admin", "admin@test.com", "adminpassword")

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
