from django.db import models
from django.conf import settings
from categories.models import Category
from users.models import CustomUser
from django.db.models import Avg
from django.utils import timezone

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='restaurants', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='restaurants', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    location = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)  # Yeni alan
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Yeni alan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    opening_time = models.TimeField(blank=True, null=True)  # Yeni alan
    closing_time = models.TimeField(blank=True, null=True)  # Yeni alan
    about = models.TextField(blank=True, null=True)  # Yeni alan
    latitude = models.FloatField()  # Enlem
    longitude = models.FloatField()  # Boylam
    photo = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def is_open(self):
        """
        Check if the restaurant is currently open based on current time.
        """
        if not self.opening_time or not self.closing_time:
            return True  # Çalışma saatleri belirtilmediyse her zaman açık
        current_time = timezone.now().time()
        return self.opening_time <= current_time <= self.closing_time


    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_rating if avg_rating else 0
        self.save()


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)  # Yeni beğeni sayacı alanı
    approved = models.BooleanField(default=False) # Moderasyon için yeni alan

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating})"
    

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorite_restaurants', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='favorites', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # Bir kullanıcı bir restoranı yalnızca bir kez favorileyebilir

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"    