

from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token

class IsNotAuthenticated(BasePermission):
    """
    Allows access only to unauthenticated users.
    """

    def has_permission(self, request, view):
        if request.user:
            v = Token.objects.filter(user=request.user)
            if len(v)==0:
                return True
            return False
        return (not bool(request.user and request.user.is_authenticated))