from . import views

from django.urls import path
from .views import ArticlesView, ArticleView


app_name = 'mainapp'

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('category/<int:pk>/', ArticlesView.as_view(), name='category'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
    path('article/create/', views.create_article, name='create_article'),
]
