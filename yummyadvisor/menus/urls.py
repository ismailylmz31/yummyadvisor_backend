from django.urls import path
from .views import (
    MenuListCreateView,
    MenuDetailView,
    DishListCreateView,
    DishDetailView,
    MenuListView,
)

urlpatterns = [
    path('', MenuListCreateView.as_view(), name='menu-list-create'),
    path('<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('list/', MenuListView.as_view(), name='menu-list'),
    path('dishes/', DishListCreateView.as_view(), name='dish-list-create'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
]
