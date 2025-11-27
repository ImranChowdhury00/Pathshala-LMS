from django.db import models
from django.core.validators import MinValueValidator
from courses.models import Course, TimeStampedModel
from users.models import User

class Enrollment(TimeStampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={'role': 'STUDENT'})
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollments')
    price = models.FloatField()

    class Meta:
        unique_together = ('student', 'course') 
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
    
class Transaction(TimeStampedModel):

    class TransactionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'
    
    enrollment = models.OneToOneField(Enrollment,  on_delete=models.SET_NULL, related_name='transaction',null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.status} transaction for {self.course.title} by {self.student.username}"



