from django.urls import path
from .views import (
    RestaurantListCreateView,
    RestaurantDetailView,
    RestaurantListView,
    RestaurantStatisticsView,
    RestaurantsWithMenuView,
    ReviewDetailView,
    ReviewListCreateView,
    ReviewLikeView,
    FavoriteRestaurantView,
    TopReviewsView,
    AdvancedRestaurantListView,
    ReviewModerationView,
    FavoriteRestaurantListCreateView,
    FavoriteRestaurantDetailView,
)

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('list/', RestaurantListView.as_view(), name='restaurant-list'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/like/<int:pk>/', ReviewLikeView.as_view(), name='review-like'),
    path('favorites/', FavoriteRestaurantListCreateView.as_view(), name='favorite-restaurant-list-create'),
    path('favorites/<int:pk>/', FavoriteRestaurantDetailView.as_view(), name='favorite-restaurant-detail'),
    path('favorites/manage/<int:restaurant_id>/', FavoriteRestaurantView.as_view(), name='favorite-restaurant-manage'),
    path('top-reviews/<int:restaurant_id>/', TopReviewsView.as_view(), name='top-reviews'),
    path('advanced-list/', AdvancedRestaurantListView.as_view(), name='advanced-restaurant-list'),
    path('review-moderation/<int:pk>/', ReviewModerationView.as_view(), name='review-moderation'),
    path('statistics/', RestaurantStatisticsView.as_view(), name='restaurant-statistics'),
    path('with-menu/', RestaurantsWithMenuView.as_view(), name='restaurants-with-menu'),
]
