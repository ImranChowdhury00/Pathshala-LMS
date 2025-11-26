from django.db import models
from users.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Category(TimeStampedModel):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    banner = models.ImageField(upload_to='course_banners/')
    duration = models.FloatField(help_text="Duration in hours or days or months")
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6,decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='courses', null=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='courses_taught', limit_choices_to={'role':'TEACHER'}, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to='lesson_videos/')
    order = models.PositiveSmallIntegerField(default=1)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        unique_together = ('course', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order} : {self.title}"
    

class Material(TimeStampedModel):

    class MaterialType(models.TextChoices):
        PDF = 'PDF', 'PDF Document'
        TEXT = 'TEXT', 'Text Content'
    
    title = models.CharField(max_length=50)
    material_type = models.CharField(max_length=10, choices=MaterialType.choices, default=MaterialType.TEXT)
    pdf_material = models.FileField(upload_to='course_materials/', blank=True, null=True)
    text_material = models.TextField(null=True, blank=True)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return f"[{self.get_material_type_display()}] {self.title}"