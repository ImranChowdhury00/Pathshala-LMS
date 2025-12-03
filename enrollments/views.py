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
    
    def update_enrollment_status(self, transaction):
        enrollment = transaction.enrollment
        if not enrollment:
            return
        if transaction.status == 'SUCCESS':
            enrollment.status = 'ACTIVE'
        elif transaction.status in ['FAILED', 'REFUNDED']:
            enrollment.status = 'CANCELLED'
        enrollment.save()   
    
    def perform_create(self, serializer):
        user = self.request.user
        status = serializer.validated_data.get('status', 'PENDING')

        if user.role == 'ADMIN':
            transaction = serializer.save(status=status)
        else:
            transaction = serializer.save(student=user,status=status)

        self.update_enrollment_status(transaction)

    def perform_update(self, serializer):
    
        transaction = serializer.save()
        self.update_enrollment_status(transaction)