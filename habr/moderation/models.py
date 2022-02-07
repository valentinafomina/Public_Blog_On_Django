from django.db import models

from mainapp.models import Article
from authapp.models import User


class ModeratorAction(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    banned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    banned_on = models.BooleanField(default=None, null=True)
