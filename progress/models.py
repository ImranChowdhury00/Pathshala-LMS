from django.db import models
from users.models import User
from courses.models import Course, Lesson, TimeStampedModel

class LessonCompletion(TimeStampedModel):

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='lesson_completed', limit_choices_to={'role': 'STUDENT'})
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completed_lesson')
    
    class Meta:
        unique_together = ('student', 'lesson')
        ordering = ['completed_at']
        verbose_name_plural = "Lesson Completions"

    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"[{status}] {self.student.username} on {self.lesson.title}"


class CourseProgress(TimeStampedModel):

    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,)
    is_course_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progresses',limit_choices_to={'role': 'STUDENT'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_progresses')
    
    class Meta:
        unique_together = ('student', 'course')
        verbose_name_plural = "Course Progresses"

    def __str__(self):
        return f"{self.student.username}'s progress in {self.course.title}: {self.progress_percentage}%"
