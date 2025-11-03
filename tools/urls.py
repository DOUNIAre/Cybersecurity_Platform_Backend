from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToolViewSet, LanguageViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'', ToolViewSet, basename='tool')

urlpatterns = [
    path('', include(router.urls)),
]