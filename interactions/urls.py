from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import QuestionViewSet, AnswerViewSet, CourseReviewViewSet, CertificateViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='question') 
router.register('answers', AnswerViewSet, basename='answer')
router.register('reviews', CourseReviewViewSet, basename='review') 
router.register('certificates', CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
]