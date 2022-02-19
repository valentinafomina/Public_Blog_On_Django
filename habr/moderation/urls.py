from django.urls import path

import mainapp.views as mainapp
from . import views
from .views import ban_article, unban_article, ban_comment, unban_comment,\
    change_moderator_status, ModeratorPage, report_article

app_name = 'moderation'


urlpatterns = [
    path('moderator_page', ModeratorPage.as_view(), name='moderator_page'),
    path('ban_article/<int:pk>/', ban_article, name='ban_article'),
    path('ban_comment/<int:pk>/', ban_comment, name='ban_comment'),
    path('unban_article/<int:pk>/', unban_article, name='unban_article'),
    path('unban_comment/<int:pk>/', unban_comment, name='unban_comment'),
    path('change_moderator_status/<int:pk>/', change_moderator_status, name='change_moderator_status'),
]