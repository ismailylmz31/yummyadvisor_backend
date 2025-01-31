from django.db import models
from restaurants.models import Restaurant

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Eğer zaman bilgisi gerekiyorsa
    available = models.BooleanField(default=True)  # Örnek boolean alan

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

class Dish(models.Model):
    menu = models.ForeignKey(Menu, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Eğer zaman bilgisi gerekiyorsa
    available = models.BooleanField(default=True)  # Örnek boolean alan
    photo = models.ImageField(upload_to='dish_photos/', blank=True, null=True)
    def __str__(self):
        return self.name
