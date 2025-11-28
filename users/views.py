from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserDetailSerializer, UserCreationSerializer , StudentRegistrationSerializer
from .permissions import IsAdmin, IsAdminOrOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreationSerializer
        return UserDetailSerializer
        
    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsAdmin]
            
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
            
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
class StudentRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentRegistrationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated] 
            
        return [permission() for permission in permission_classes]