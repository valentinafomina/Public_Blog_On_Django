from django.urls import path

from . import views
from .views import ArticlesView, ArticleView, ArticleCreateView


app_name = 'mainapp'

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('category/<int:pk>/', ArticlesView.as_view(), name='category'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
    path('article/create/', ArticleCreateView.as_view(), name='create_article'),
]
