from django.urls import path
from .views import UserDetailView, UserCreateView, UserUpdateView, UserDeleteView, login, logout

app_name = 'auth'

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('users-detail/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users-create/', UserCreateView.as_view(), name='users_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='users_update'),
    path('users-remove/<int:pk>/', UserDeleteView.as_view(), name='users_remove'),
]