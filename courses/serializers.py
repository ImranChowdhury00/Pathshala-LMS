from rest_framework import serializers
from .models import Category, Course, Lesson, Material


class CategorySerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(many=True, read_only = True)

    class Meta:
        model = Category
        fields = ['id','name','slug','created_at','updated_at','courses']
        read_only_fields =['slug']


class CourseSerializer(serializers.ModelSerializer):
    # instructor_detail = UserDetailSerializer(source='instructor', read_only=True)
    lessons = serializers.StringRelatedField(many=True, read_only = True)
    category = serializers.StringRelatedField()
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id','title','slug','category','instructor','banner','description','duration','is_active','price','lessons','created_at','updated_at']
        read_only_fields = ('instructor',)


class LessonSerializer(serializers.ModelSerializer):
    materials = serializers.StringRelatedField(many=True, read_only = True)
    course = serializers.StringRelatedField()
    class Meta:
        model = Lesson
        fields = ['id','order','title','description','video','course','materials','created_at','updated_at']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'