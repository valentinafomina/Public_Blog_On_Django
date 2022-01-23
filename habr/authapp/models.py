from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_about = models.CharField(max_length=1024)
    avatar_link = models.ImageField(upload_to='users_images', blank=True)
    blocked_time = models.DateTimeField()
