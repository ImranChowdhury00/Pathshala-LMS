from rest_framework import viewsets
from .models import Category, Course, Lesson , Material
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer , MaterialSerializer
from users.permissions import IsAdmin, IsTeacher , IsAdminOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsCourseInstructor

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'TEACHER']:
            return Course.objects.all().order_by('-created_at')
        
        return self.queryset

    def perform_create(self, serializer):
        if self.request.user.role == 'TEACHER':
            serializer.save(instructor=self.request.user)
        else:
            serializer.save()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
            
        elif self.action == 'create':
            permission_classes = [IsAdmin, IsTeacher] 
            
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsCourseInstructor, IsAdmin] 
            
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]


class lessonViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Lesson.objects.filter(course=course_id)
    
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
            
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsCourseInstructor, IsAdmin] 
            
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]

class MaterialViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return Material.objects.filter(lesson=lesson_id)

    serializer_class = MaterialSerializer
