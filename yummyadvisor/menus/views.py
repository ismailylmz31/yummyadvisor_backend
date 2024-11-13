from rest_framework import generics, permissions
from restaurants.models import Restaurant
from .models import Menu, Dish
from .serializers import MenuSerializer, DishSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import PermissionDenied

class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        restaurant = Restaurant.objects.filter(id=restaurant_id).first()

        if not restaurant:
            raise PermissionDenied("Invalid restaurant.")

        # Check if the user is the owner of the restaurant or an admin
        if not (self.request.user == restaurant.owner or self.request.user.is_admin):
            raise PermissionDenied("You do not have permission to add a menu to this restaurant.")

        serializer.save(restaurant=restaurant)

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser]

class DishListCreateView(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminUser]
