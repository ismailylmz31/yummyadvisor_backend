from rest_framework import serializers
from .models import Restaurant
from .models import Review
from .models import FavoriteRestaurant

class RestaurantSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'category', 'owner', 'rating', 'location', 'address', 'contact_number', 'created_at', 'updated_at', 'total_reviews']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_total_reviews(self, obj):
        return obj.reviews.count()  # İlgili restoranın yorum sayısını döndürür
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'restaurant', 'created_at']

class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRestaurant
        fields = ['id', 'user', 'restaurant']
        read_only_fields = ['user']  