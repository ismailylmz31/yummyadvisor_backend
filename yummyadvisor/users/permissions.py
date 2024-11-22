from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsManager(BasePermission):
    """
    Allow access only to manager users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsModerator(BasePermission):
    """
    Allow access only to moderator users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator
