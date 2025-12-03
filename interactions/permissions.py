from rest_framework import permissions

class IsStudentOwner(permissions.BasePermission):
    message = "You must be the student who created this resource."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user == obj.student

class IsResponderOrAdmin(permissions.BasePermission):
    """
    Allows Admin or the Answer's Responder (Teacher) to modify the Answer object.
    Students cannot modify Answers.
    """
    message = "You must be the responder of this answer or an Admin."

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.role == 'ADMIN':
            return True

        # Safe methods (read) are allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write access (PUT, DELETE) requires the user to be the original responder (Teacher/Admin)
        return obj.responder == request.user

class IsCertificateOwnerOrAdmin(permissions.BasePermission):
    message = "You are not authorized to view this certificate."

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == 'ADMIN':
            return True

        return obj.student == request.user

class IsAdminOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_staff or obj.student == request.user
    
class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role == "TEACHER" or user.role == "ADMIN")