from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class UserManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            query = query.casefold()
            query = query.capitalize()
            or_lookup = (Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
            qs = qs.filter(or_lookup)
        return qs


class User(AbstractUser):
    user_about = models.CharField(max_length=1024, blank=True)
    avatar_link = models.ImageField(upload_to='users_images', blank=True)
    blocked_time = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(blank=True, unique=True)
    likes = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_likes')
    model_name = models.CharField(max_length=12, default='user')
