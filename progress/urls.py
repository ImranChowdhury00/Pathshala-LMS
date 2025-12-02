from rest_framework.routers import DefaultRouter
from .views import LessonCompletionViewSet, CourseProgressViewSet

router = DefaultRouter()
router.register("lesson-completions", LessonCompletionViewSet, basename="lesson-completion")
router.register("course-progress", CourseProgressViewSet, basename="course-progress")

urlpatterns = router.urls
