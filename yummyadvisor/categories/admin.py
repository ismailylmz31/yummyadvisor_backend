from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Görüntülenecek sütunlar
    search_fields = ('name',)
    list_filter = ('created_at',)
