from django.urls import path
from .views import RestaurantListCreateView, RestaurantDetailView
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
