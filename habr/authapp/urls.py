from django.urls import path
from .views import UserDetailView, UserCreateView, UserUpdateView, UserDeleteView, logout, UserLoginView

app_name = 'auth'

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('login/', login, name='login'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('reg/', UserCreateView.as_view(), name='users_create'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='users_update'),
    path('remove/<int:pk>/', UserDeleteView.as_view(), name='users_remove'),
]
