from rest_framework import permissions

class IsCourseInstructor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.role == 'ADMIN':
            return True
            
        if request.user.role == 'TEACHER':
            return obj.instructor == request.user
            
        return False