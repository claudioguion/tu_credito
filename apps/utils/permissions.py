from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Global permission: read-only for unauthenticated users.
    Write actions require authentication.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user and request.user.is_authenticated)
