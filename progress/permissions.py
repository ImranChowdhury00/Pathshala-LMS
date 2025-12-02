from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role == "ADMIN":
            return True

        if request.method in SAFE_METHODS:
            return obj.student == request.user

        return False

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return False

        return request.user.is_authenticated
    

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.student == request.user
