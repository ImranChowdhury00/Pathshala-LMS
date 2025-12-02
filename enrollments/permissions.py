from rest_framework import permissions

class IsAdminOrEnrolled(permissions.BasePermission):

    def has_object_permission(self, request, view, obj): 
        if request.user.role == 'ADMIN':
            return True
            
        if request.user.role == 'STUDENT':
            return obj.student == request.user
            
        return False