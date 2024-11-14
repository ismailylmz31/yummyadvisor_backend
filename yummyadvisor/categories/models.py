from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Eğer zaman bilgisi gerekiyorsa
    available = models.BooleanField(default=True)  # Örnek boolean alan

    def __str__(self):
        return self.name
