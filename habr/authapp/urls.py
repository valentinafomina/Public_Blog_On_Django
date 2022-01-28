from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, login

app_name = 'auth'

urlpatterns = [
    path('login/', login, name='login'),
    path('users-read/', UserListView.as_view(), name='users_read'),
    path('users-create/', UserCreateView.as_view(), name='users_create'),
    path('users-update/', UserUpdateView.as_view(), name='users_update'),
    path('users-remove/', UserDeleteView.as_view(), name='users_remove'),
]