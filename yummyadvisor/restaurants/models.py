from django.db import models
from django.conf import settings
from categories.models import Category
from users.models import CustomUser

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='restaurants', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='restaurants', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating})"