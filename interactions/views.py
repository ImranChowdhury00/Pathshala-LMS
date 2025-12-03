from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStudent , IsTeacher, IsAdmin
from rest_framework import status
from .models import Question, Answer, CourseReview, Certificate
from .serializers import (
    QuestionSerializer, 
    AnswerSerializer, 
    CourseReviewSerializer, 
    CertificateSerializer
)
from .permissions import IsStudentOwner,  IsResponderOrAdmin, IsCertificateOwnerOrAdmin , IsAdminOrOwner, IsTeacherOrAdmin
from users.permissions import IsAdmin # Assuming IsAdmin is imported from users


# --- Helper for setting owner automatically ---
def set_request_user_as_owner(serializer):
    """Sets the 'student' or 'responder' field based on the request user."""
    if hasattr(serializer.instance, 'student'):
        serializer.save(student=serializer.context['request'].user)
    elif hasattr(serializer.instance, 'responder'):
        serializer.save(responder=serializer.context['request'].user)
    else:
        serializer.save()


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, IsStudentOwner]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    def get_queryset(self):
        queryset = self.queryset
        lesson_id = self.request.query_params.get('lesson_id')
        
        if lesson_id:
            queryset = queryset.filter(lesson__id=lesson_id)
            
        return queryset


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all().order_by('created_at')
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsTeacherOrAdmin()]
        
        return [IsAuthenticated(), IsResponderOrAdmin()]

    def perform_create(self, serializer):
        answer_instance = serializer.save(responder=self.request.user)
        question = answer_instance.question
        if not question.is_resolved:
            question.is_resolved = True
            question.save(update_fields=['is_resolved'])


class CourseReviewViewSet(viewsets.ModelViewSet):
    queryset = CourseReview.objects.all().order_by('-created_at')
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if not course.enrollments.filter(student=self.request.user, status='ACTIVE').exists():
             raise Response(
                 {"detail": "You must be enrolled in this course to leave a review."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(student=self.request.user)

    def get_queryset(self):
        return self.queryset


class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    queryset = Certificate.objects.all().order_by('-issue_date')

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == 'ADMIN':
            return self.queryset

        if user.is_authenticated and user.role == 'STUDENT':
            return self.queryset.filter(student=user)
            
        return self.queryset.none()
    
    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return [IsAuthenticated, IsCertificateOwnerOrAdmin()]

    #     return [IsAdmin()]
