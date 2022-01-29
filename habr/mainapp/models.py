from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils import timezone


class ArticleCategory(models.Model):
    name = models.CharField(
        verbose_name='имя',
        max_length=64,
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='активный'
    )

    def __str__(self):
        return self.name


class Article(models.Model):

    # CATEGORY_CHOICES = (
    #     ("DESIGN", "Design"),
    #     ("WEB_DEV", "Web Development"),
    #     ("MOBILE_DEV", "Mobile Development"),
    #     ("MARKETING", "Marketing"),
    # )

    # Django based user, to be deleted upon creation of custom User model
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    article_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_banned = models.BooleanField(default=None, null=True)
    category = models.ForeignKey(ArticleCategory, verbose_name='Категория',
                                 on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
