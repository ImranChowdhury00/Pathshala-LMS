from django.contrib import admin
from .models import Course, Category, Lesson, Material

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Material)
