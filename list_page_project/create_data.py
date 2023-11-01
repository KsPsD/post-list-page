import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "list_page_project.settings")
django.setup()

from django.contrib.auth.models import User
from posts.models import Comment, Post

# Create superuser
superuser_username = "admin"
superuser_email = "admin@example.com"
superuser_password = "password"

if not User.objects.filter(username=superuser_username).exists():
    user = User.objects.create_superuser(
        superuser_username, superuser_email, superuser_password
    )
    print("Superuser created.")
else:
    user = User.objects.get(username=superuser_username)
    print("Superuser already exists.")


for i in range(25):
    post_title = f"Test Post {i}"
    post_content = f"This is test post content {i}"
    comment_content = f"This is test comment content {i}"

    post, created = Post.objects.get_or_create(
        title=post_title, author=user, defaults={"content": post_content}
    )
    if created:
        print(f"Test post {i} created.")

    comment, created = Comment.objects.get_or_create(
        post=post, author=user, defaults={"content": comment_content}
    )
    if created:
        print(f"Test comment for post {i} created.")
