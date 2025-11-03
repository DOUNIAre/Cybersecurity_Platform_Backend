from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Tool, Language
from .serializers import ToolListSerializer, ToolDetailSerializer, ToolCreateSerializer, LanguageSerializer

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'slug'

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.filter(status='approved')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories__slug', 'languages__slug', 'is_featured']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['stars_count', 'views_count', 'created_at', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ToolDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ToolCreateSerializer
        return ToolListSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        trending_tools = Tool.objects.filter(status='approved').order_by('-stars_count')[:10]
        serializer = ToolListSerializer(trending_tools, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recently_updated(self, request):
        recent_tools = Tool.objects.filter(status='approved').order_by('-last_updated')[:10]
        serializer = ToolListSerializer(recent_tools, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def increment_views(self, request, slug=None):
        tool = self.get_object()
        tool.views_count += 1
        tool.save(update_fields=['views_count'])
        return Response({'views_count': tool.views_count})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def star(self, request, slug=None):
        tool = self.get_object()
        tool.stars_count += 1
        tool.save(update_fields=['stars_count'])
        return Response({'stars_count': tool.stars_count})
