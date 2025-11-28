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

# class IsAdminOrReadOnly(permissions.BasePermission):
#     """
#     Admin users can perform any action (full CRUD).
#     Other authenticated users can only perform read-only actions (GET, HEAD, OPTIONS).
#     """
#     def has_permission(self, request, view):
#         # Allow GET, HEAD, OPTIONS requests for anyone authenticated
#         if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
#             return True
        
#         # Allow all methods only for Admin
#         return bool(request.user and request.user.role == 'ADMIN')

