from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    liked_posts = models.ManyToManyField("Post", related_name="likes")
    following = models.ManyToManyField("User", related_name="users_followed")


class Post(models.Model):
    content = models.TextField(blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_author")

# Do not forget to run "python manage.py makemigrations" and then "python manage.py migrate"
# after any changes are made to this file. 

