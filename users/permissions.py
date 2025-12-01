from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == 'TEACHER')

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == 'STUDENT')
    
class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
    
        return obj == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

