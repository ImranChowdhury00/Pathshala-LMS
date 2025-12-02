from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EnrollmentViewSet, TransactionViewSet

router = DefaultRouter()
router.register('enrollments', EnrollmentViewSet, basename='enrollments')
router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
]
