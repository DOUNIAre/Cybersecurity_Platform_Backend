from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToolSubmissionViewSet

router = DefaultRouter()
router.register(r'', ToolSubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]