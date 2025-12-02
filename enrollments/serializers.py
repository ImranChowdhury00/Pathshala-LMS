from rest_framework import serializers
from .models import Enrollment, Transaction
from users.serializers import UserDetailSerializer
from courses.serializers import CourseSerializer

class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, read_only=True)

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255, read_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    student_detail = UserDetailSerializer(source='student', read_only=True)
    course_detail = CourseSerializer(source='course', read_only=True)
    enrollment = serializers.StringRelatedField()
    
    class Meta:
        model = Transaction
        fields = ['id', 'enrollment', 'amount', 'status', 'transaction_id', 'student_detail', 'course_detail', 'created_at']
        read_only_fields = ('student', 'course', 'amount', 'transaction_id', 'status')


class EnrollmentSerializer(serializers.ModelSerializer):
    student_details = UserDetailSerializer(source='student', read_only = True)
    course_details = CourseSerializer(source ='course', read_only = True)
    class Meta:
        model = Enrollment
        fields= ['id', 'price', 'status', 'student_details', 'course_details', 'created_at']
        read_only_fields = ('student', 'price')
