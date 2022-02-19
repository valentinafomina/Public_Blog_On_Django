from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import redirect
from django.urls import resolve

from mainapp.models import Article, Comment
from authapp.models import User

OBJECT_CHOICES = (
    (Comment, "Comment"),
    (Article, "Article"),
)


class BannedObjects(models.Model):

    banned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    banned_on = models.DateTimeField(blank=True, null=True)
    banned_article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    banned_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def create(cls, object_pk, user):
        object_category = object_pk.__class__
        if object_category == Article:
            ban = cls(banned_by=user,
                      banned_on=datetime.now(),
                      banned_article=object_pk)
            return ban
        if object_category == Comment:
            ban = cls(banned_by=user,
                      banned_on=datetime.now(),
                      banned_comment=object_pk)
            return ban

    def get_object_name(self, object_pk):
        self.object_category = object_pk.__class__
        if self.object_category == Article:
            object_name = self.banned_article.title
            return object_name

        elif self.object_category == Comment:
            object_name = self.banned_comment.article.title
            return object_name

    def get_article_author(self):
        author = self.banned_article.user
        return author

    def get_object_owner(self):
        author = self.banned_object.author
        return author


class Report(models.Model):
    reported_article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    reported_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_on = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def create(cls, object_pk, user):
        object_category = object_pk.__class__
        if object_category == Article:
            report = cls(reported_by=user,
                         reported_on=datetime.now(),
                         reported_article=object_pk)
            return report
        if object_category == Comment:
            report = cls(reported_by=user,
                         reported_on=datetime.now(),
                         reported_comment=object_pk)
            return report






