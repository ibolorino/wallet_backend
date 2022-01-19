from rest_framework import permissions

class IsAadminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_authenticated and request.method in permissions.SAFE_METHODS) or
            (request.user and request.user.is_staff)
        )