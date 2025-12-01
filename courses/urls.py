from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, CourseViewSet, lessonViewSet, MaterialViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('', CourseViewSet, basename='courses')
router.register(r'(?P<course_id>\d+)/lessons', lessonViewSet, basename='course-lesson')
router.register(r'(?P<course_id>\d+)/lessons/(?P<lesson_id>\d+)/materials', MaterialViewSet, basename='lesson-material')

urlpatterns = [
    path('', include(router.urls)),
]
