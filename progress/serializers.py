from rest_framework import serializers
from .models import LessonCompletion, CourseProgress

class LessonCompletionSerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField(default=True)
    class Meta:
        model = LessonCompletion
        fields = '__all__'
        read_only_fields = ['student', 'completed_at', 'created_at', 'updated_at']


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = '__all__'
        read_only_fields = ['student','progress_percentage','is_course_completed','completed_at','created_at','updated_at']
