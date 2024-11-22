from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Yalnızca admin kullanıcıların yazma izni var.
    Diğer herkes sadece okuma (GET) iznine sahip.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS gibi istekler
            return True
        return request.user.is_authenticated and request.user.is_staff
