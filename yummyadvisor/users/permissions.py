from rest_framework.permissions import BasePermission

class IsAuthenticatedAnd(BasePermission):
    """
    Custom base permission to combine authentication with other roles.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdmin(IsAuthenticatedAnd):
    """
    Allow access only to admin users.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin


class IsManager(IsAuthenticatedAnd):
    """
    Allow access only to manager users.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_manager


class IsModerator(IsAuthenticatedAnd):
    """
    Allow access only to moderator users.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_moderator
