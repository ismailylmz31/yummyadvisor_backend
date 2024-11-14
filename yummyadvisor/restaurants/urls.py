from django.urls import path
from .views import RestaurantListCreateView, RestaurantDetailView
from .views import ReviewListCreateView, ReviewDetailView
from .views import FavoriteRestaurantListCreateView, FavoriteRestaurantDetailView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('favorites/', FavoriteRestaurantListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:pk>/', FavoriteRestaurantDetailView.as_view(), name='favorite-detail'),
]
