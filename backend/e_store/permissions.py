

from rest_framework import permissions
from rest_framework.authtoken.models import Token

class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to unauthenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)
    
    
class ReviewPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.action in ['create','destroy']:
                return False
        return True
            
            