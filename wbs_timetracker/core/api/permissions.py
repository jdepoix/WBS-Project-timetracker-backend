from rest_framework.permissions import BasePermission


class IsAuthenticatedOrPostOnly(BasePermission):
    """
    if user is not authenticated, only POST is allowed
    """
    SAFE_METHODS = ('POST', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        return (
            request.method in IsAuthenticatedOrPostOnly.SAFE_METHODS or
            request.user and
            request.user.is_authenticated()
        )
