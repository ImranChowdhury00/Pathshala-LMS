from rest_framework import viewsets
from .models import Enrollment, Transaction
from .serializers import EnrollmentSerializer, TransactionSerializer
from users.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrEnrolled

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().order_by('-created_at')
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'ADMIN':
            return self.queryset.all()
        
        elif user.is_authenticated and user.role == 'STUDENT':
            return self.queryset.filter(student=user)
        
        return self.queryset.none() 
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        
        return [IsAuthenticated(), IsAdminOrEnrolled()]
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'STUDENT':
            serializer.save(student=user, status='PENDING')
        else:
            serializer.save()

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'ADMIN':
            return self.queryset
        
        if user.is_authenticated and user.role == 'STUDENT':
            return self.queryset.filter(student=user)
        
        return self.queryset.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        
        return [IsAuthenticated(), IsAdminOrEnrolled()]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(student=user, status='PENDING')

    def perform_update(self, serializer):
    
        transaction = serializer.save()

        enrollment = transaction.enrollment
        if enrollment:
            if transaction.status == 'SUCCESS':
                enrollment.status = 'ACTIVE'
            elif transaction.status in ['FAILED', 'REFUNDED']:
                enrollment.status = 'CANCELLED'
            enrollment.save()