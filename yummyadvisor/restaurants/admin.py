from django.contrib import admin
from .models import Restaurant, Review

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'rating', 'location')
    search_fields = ('name', 'location')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review)
