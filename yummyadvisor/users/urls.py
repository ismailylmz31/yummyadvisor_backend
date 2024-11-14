from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserListView,
    PasswordChangeView,
    UserProfileView,
    UserProfileUpdateView,
    FavoriteRestaurantListView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('favorites/', FavoriteRestaurantListView.as_view(), name='favorite-restaurant-list'),
]
