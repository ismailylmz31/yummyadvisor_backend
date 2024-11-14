from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Optional: Customizing the admin display
    list_display = ['username', 'email', 'is_admin', 'is_manager', 'is_moderator']
    list_filter = ['is_admin', 'is_manager', 'is_moderator']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_manager', 'is_moderator')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin', 'is_manager', 'is_moderator')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
