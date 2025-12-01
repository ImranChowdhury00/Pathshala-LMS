from rest_framework import serializers
from .models import Category, Course, Lesson, Material


class CategorySerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(many=True, read_only = True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields =['slug']


class CourseSerializer(serializers.ModelSerializer):
    # instructor_detail = UserDetailSerializer(source='instructor', read_only=True)
    lessons = serializers.StringRelatedField(many=True, read_only = True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('instructor',)


class LessonSerializer(serializers.ModelSerializer):
    materials = serializers.StringRelatedField(many=True, read_only = True)
    class Meta:
        model = Lesson
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'