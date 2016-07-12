from rest_framework.permissions import BasePermission

class IsAuthenticatedOrOptionsOnly(BasePermission):
    """
    if user is not authenticated, only OPTIONS is allowed
    """
    def has_permission(self, request, view):
        return (
            request.method in self.safe_methods or
            request.user and
            request.user.is_authenticated()
        )

    @property
    def safe_methods(self):
        return ('OPTIONS',)


class IsAuthenticatedOrPostOnly(IsAuthenticatedOrOptionsOnly):
    """
    if user is not authenticated, only POST is allowed
    """
    @property
    def safe_methods(self):
        return ('POST', 'HEAD', 'OPTIONS',)
