from django.contrib import admin
from .models import Article, ArticleCategory, Comment

admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(Comment)