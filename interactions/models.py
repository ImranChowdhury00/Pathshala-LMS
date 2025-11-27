from django.db import models
from users.models import User
from courses.models import Course, Lesson, TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator

class Question(TimeStampedModel):
    question = models.TextField()
    is_resolved = models.BooleanField(default=False)

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', limit_choices_to={'role': 'STUDENT'})
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    
    def __str__(self):
        return f"Q:by {self.student.username}"
    
class Answer(TimeStampedModel):
    answer = models.TextField()

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers_provided')

    def __str__(self):
        return f"A: by {self.responder.username}"
    

class CourseReview(TimeStampedModel):
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(null=True, blank=True)

    student = models.ForeignKey( User, on_delete=models.SET_NULL, related_name='reviews', limit_choices_to={'role': 'STUDENT'}, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"Review by {self.student.username} for {self.course.title} - {self.rating}/5"
    

class Certificate(TimeStampedModel):
    unique_id = models.CharField(max_length=50, unique=True, editable=False)
    certificate = models.FileField(upload_to='certificates/',null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)

    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='certificate', limit_choices_to={'role': 'STUDENT'})
    course = models.OneToOneField(Course,on_delete=models.CASCADE, related_name='certificate')    

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-issue_date']

    def __str__(self):
        return f"Certificate for {self.student.username} in {self.course.title}"
        