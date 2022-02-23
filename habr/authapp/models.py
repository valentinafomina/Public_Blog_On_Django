from django.contrib.auth.models import AbstractUser
from django.db import models

from mainapp.mixins import ModelClassNameMixin


class User(AbstractUser, ModelClassNameMixin):
    user_about = models.CharField(max_length=1024, blank=True)
    avatar_link = models.ImageField(upload_to='users_images', blank=True)
    blocked_time = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(blank=True, unique=True)
    likes = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_likes')

