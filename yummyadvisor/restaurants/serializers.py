from rest_framework import serializers
from .models import Restaurant
from .models import Review
from .models import FavoriteRestaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'category', 'owner', 'rating', 'location']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRestaurant
        fields = ['id', 'user', 'restaurant']        