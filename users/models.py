from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField('Role', max_length=10, choices=UserRole.choices, default= UserRole.STUDENT)
    mobile_no = models.CharField(max_length=15,blank=True, null=True, unique=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN or self.is_superuser
    
    @property
    def is_teacher(self):
        return self.role == self.UserRole.TEACHER
    
    @property
    def is_student(self):
        return self.role == self.UserRole.STUDENT
    

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']


    def __str__(self):
        return f"{self.username} - ({self.get_role_display()})"