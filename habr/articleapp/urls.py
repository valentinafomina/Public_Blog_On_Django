from django.urls import path
from . import views


urlpatterns = [
    path('create_article', views.create_article, name='create_article'),
]
