from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils import timezone


class Article(models.Model):

    CATEGORY_CHOICES = (
        ("DESIGN", "Design"),
        ("WEB_DEV", "Web Development"),
        ("MOBILE_DEV", "Mobile Development"),
        ("MARKETING", "Marketing"),
    )

    # Django based user, to be deleted upon creation of custom User model
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    article_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_banned = models.BooleanField(default=None, null=True)
    category = models.CharField(max_length=12,
                  choices=CATEGORY_CHOICES,
                  default="WEB_DEV")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
