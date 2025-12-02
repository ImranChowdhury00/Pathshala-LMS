from rest_framework import viewsets
from django.utils import timezone
from .models import LessonCompletion, CourseProgress
from .serializers import LessonCompletionSerializer, CourseProgressSerializer
from .permissions import IsAdminOrOwner, IsOwnerOrReadOnly
from courses.models import Lesson


class LessonCompletionViewSet(viewsets.ModelViewSet):
    queryset = LessonCompletion.objects.all()
    serializer_class = LessonCompletionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_save(self, student, lesson, is_completed=True):
        completion, _ = LessonCompletion.objects.get_or_create(student=student,lesson=lesson)
        completion.is_completed = is_completed

        if is_completed and not completion.completed_at:
            completion.completed_at = timezone.now()

        completion.save()
        self.update_course_progress(student, lesson.course)

        return completion


    def perform_create(self, serializer):
        student = self.request.user
        lesson = serializer.validated_data["lesson"]
        is_completed = serializer.validated_data.get("is_completed", True)

        self.perform_save(student, lesson, is_completed)

    def perform_update(self, serializer):
        completion = serializer.save()
        self.perform_save(completion.student, completion.lesson, completion.is_completed)


    def update_course_progress(self, student, course):
        total_lessons = Lesson.objects.filter(course=course).count()
        completed_lessons = LessonCompletion.objects.filter(student=student,lesson__course=course,is_completed=True).count()
        
        percent = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        progress, _ = CourseProgress.objects.get_or_create(student=student, course=course)
        progress.progress_percentage = round(percent, 2)

        if completed_lessons == total_lessons and total_lessons > 0:  # if course is fully completed
            progress.is_course_completed = True
            if not progress.completed_at:
                progress.completed_at = timezone.now()
        else:
            progress.is_course_completed = False

        progress.save()


class CourseProgressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseProgress.objects.all()
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == "ADMIN":
            return CourseProgress.objects.all()
        
        if user.role == "STUDENT":
            return CourseProgress.objects.filter(student=user)

        return CourseProgress.objects.none()
