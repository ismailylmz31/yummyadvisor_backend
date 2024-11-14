from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)  # Yeni rol
