from django.contrib import admin
from .models import Restaurant, Review, FavoriteRestaurant

# Modellerimizi admin paneline kaydediyoruz.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner','category', 'rating', 'location','address', 'contact_number', 'created_at', 'is_open', 'opening_time', 'closing_time')  # Görüntülenecek sütunlar
    search_fields = ('name', 'address', 'description')  # Arama yapılacak alanlar
    list_filter = ('category', 'rating')  # Filtreleme seçenekleri

    def is_open_display(self, obj):
        return "Open" if obj.is_open() else "Closed"
    is_open_display.short_description = 'Open Status'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'approved', 'created_at')  # Görüntülenecek sütunlar
    search_fields = ('restaurant__name', 'content')  # Arama yapılacak alanlar
    list_filter = ('approved', 'rating')  # Filtreleme seçenekleri

@admin.register(FavoriteRestaurant)
class FavoriteRestaurantAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant')  # Görüntülenecek sütunlar
