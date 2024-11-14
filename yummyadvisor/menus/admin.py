from django.contrib import admin
from .models import Menu, Dish

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'created_at')  # Görüntülenecek sütunlar
    search_fields = ('name', 'description')
    list_filter = ('restaurant',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'price', 'available')  # Görüntülenecek sütunlar
    search_fields = ('name', 'description')
    list_filter = ('available',)
