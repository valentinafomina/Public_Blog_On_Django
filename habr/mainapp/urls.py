from django.urls import path

import mainapp.views as mainapp
from . import views
from .views import ArticlesView, ArticleView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = 'mainapp'

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('category/<int:pk>/', ArticlesView.as_view(), name='category'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
    path('article/create/', ArticleCreateView.as_view(), name='create_article'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete_article'),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(), name='update_article'),
    path('about_us/', mainapp.about_us, name='about_us')
]
