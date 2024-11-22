from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allow only admins to perform write operations, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmin(BasePermission):
    """
    Allow only owners or admins to edit objects.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.is_admin or obj.owner == request.user)


class IsManager(BasePermission):
    """
    Allow managers to manage their own restaurants.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_manager and obj.owner == request.user
