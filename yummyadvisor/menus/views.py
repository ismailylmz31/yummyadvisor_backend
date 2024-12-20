from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from restaurants.models import Restaurant
from .permissions import IsOwnerOrAdmin
from .models import Menu, Dish
from .serializers import MenuSerializer, DishSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from restaurants.models import Restaurant


class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['restaurant__name', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'restaurant__name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # Check permissions with a custom method
        if not IsOwnerOrAdmin().has_object_permission(self.request, self, restaurant):
            raise PermissionDenied("You do not have permission to add a menu to this restaurant.")

        serializer.save(restaurant=restaurant)

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser]

class DishListCreateView(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        menu_id = self.request.data.get('menu_id')
        menu = get_object_or_404(Menu, id=menu_id)

        # Kullanıcı menünün bağlı olduğu restoranın sahibi mi?
        if not IsOwnerOrAdmin().has_object_permission(self.request, self, menu.restaurant):
            raise PermissionDenied("You do not have permission to add a dish to this menu.")

        serializer.save(menu=menu)

class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminUser]

class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all().select_related('restaurant').prefetch_related('dishes')
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['restaurant__name', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'restaurant__name']


