from rest_framework import serializers
from .models import Question, Answer, CourseReview, Certificate
from courses.models import Course 
from django.db import transaction
import uuid 

class AnswerSerializer(serializers.ModelSerializer):
    responder_username = serializers.CharField(source='responder.username', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'answer', 'question', 'responder', 'responder_username', 'created_at']
        read_only_fields = ['responder'] 


class QuestionSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'lesson', 'student', 'student_username', 'question', 'is_resolved', 'created_at', 'answers']


class CourseReviewSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = ['id', 'rating', 'review', 'student', 'student_username', 'course', 'course_title', 'created_at']


class CertificateSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'unique_id', 'certificate', 'issue_date', 'student', 'student_username', 'course', 'course_title']
        read_only_fields = ['unique_id', 'issue_date']
        