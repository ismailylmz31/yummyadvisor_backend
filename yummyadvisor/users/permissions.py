from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    """
    Custom permission to allow only managers or admins to access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_manager)
