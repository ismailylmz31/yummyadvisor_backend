from rest_framework import serializers
from .models import Menu, Dish
from decimal import Decimal

class DishSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.00'))
    menu_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Dish
        fields = ['id', 'name', 'price', 'description', 'menu_id', 'available', 'photo']
        read_only_fields = ['menu']

class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'name', 'description', 'dishes', 'available']
