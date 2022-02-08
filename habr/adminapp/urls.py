from django.urls import path
from . import views
from .views import moderator_cab

import adminapp.views

app_name = 'adminapp'


urlpatterns = [
    path('moderation/', adminapp.views.moderator_cab, name='Админка')
]