from django.urls import path

import mainapp.views as mainapp
from . import views
from .views import ban_article, unban_article, change_moderator_status, ModeratorPage

app_name = 'moderation'


urlpatterns = [
    path('moderator_page', ModeratorPage.as_view(), name='moderator_page'),
    path('ban_article/<int:pk>/', ban_article, name='ban_article'),
    path('unban_article/<int:pk>/', unban_article, name='unban_article'),
    path('change_moderator_status/<int:pk>/', change_moderator_status, name='change_moderator_status'),
               ]