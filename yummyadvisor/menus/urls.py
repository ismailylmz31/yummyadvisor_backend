from django.urls import path
from .views import MenuListCreateView, MenuDetailView, DishListCreateView, DishDetailView

urlpatterns = [
    path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('dishes/', DishListCreateView.as_view(), name='dish-list-create'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
]
