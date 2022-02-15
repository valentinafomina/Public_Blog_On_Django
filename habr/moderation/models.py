from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.db import models
from django.shortcuts import redirect

from mainapp.models import Article, Comment
from authapp.models import User

# OBJECT_CHOICES = (
#     ("COMMENT", "Comment"),
#     ("USER", "User"),
#     ("ARTICLE", "Article"),
# )


class BannedObjects(models.Model):
    banned_object = models.ForeignKey(Comment or Article, on_delete=models.CASCADE)
    banned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    banned_on = models.DateTimeField(blank=True, null=True)

    @classmethod
    def create(cls, object_pk, user):
        ban = cls(banned_object=object_pk,
                  banned_by=user,
                  banned_on=datetime.now())
        return ban

    def get_object_name(self):
        object_name = self.banned_object.title
        return object_name

    def get_object_owner(self):
        author = self.banned_object.user
        return author


class Report(models.Model):
    object = models.ForeignKey(Comment or Article, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_on = models.DateTimeField(blank=True, null=True)