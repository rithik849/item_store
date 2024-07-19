from rest_framework import permissions
class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to unauthenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)
    
    
class ReviewPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in ['POST','DELETE']:
            if request.user and request.user.is_authenticated:
                return True
        if request.method in ['GET']:
            return True
        return False
    
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.customer == request.user
    
class IsOwnerPermission(permissions.IsAuthenticated):
    
    
    def has_object_permission(self,request,view,obj):
        return obj.customer == request.user
        
class IsCustomerPermission(permissions.IsAuthenticated):
    
    def has_object_permission(self,request,view,obj):
        return obj == request.user
            