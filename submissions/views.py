from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from tools.models import Tool
from categories.models import Category
from .models import ToolSubmission
from .serializers import ToolSubmissionSerializer, ToolSubmissionCreateSerializer, ToolSubmissionReviewSerializer

class ToolSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ToolSubmission.objects.all()
    serializer_class = ToolSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ToolSubmission.objects.all()
        return ToolSubmission.objects.filter(submitter=user)

    @action(detail=False, methods=['post'])
    def create_submission(self, request):
        serializer = ToolSubmissionCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tool = Tool.objects.create(
                    name=serializer.validated_data['tool_name'],
                    description=serializer.validated_data['description'],
                    short_description=serializer.validated_data['short_description'],
                    github_url=serializer.validated_data['github_url'],
                    website_url=serializer.validated_data.get('website_url', ''),
                    creator=request.user,
                    status='pending'
                )
                
                tool.categories.set(serializer.validated_data['category_ids'])
                tool.languages.set(serializer.validated_data['language_ids'])
                
                submission = ToolSubmission.objects.create(
                    tool=tool,
                    submitter=request.user
                )
                
                return Response(
                    ToolSubmissionSerializer(submission).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        submission = self.get_object()
        serializer = ToolSubmissionReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            submission.status = 'approved'
            submission.tool.status = 'approved'
            submission.reviewer = request.user
            submission.reviewed_at = timezone.now()
            submission.review_notes = serializer.validated_data.get('review_notes', '')
            
            submission.save()
            submission.tool.save()
            
            return Response(ToolSubmissionSerializer(submission).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        submission = self.get_object()
        serializer = ToolSubmissionReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            submission.status = 'rejected'
            submission.tool.status = 'rejected'
            submission.reviewer = request.user
            submission.reviewed_at = timezone.now()
            submission.review_notes = serializer.validated_data.get('review_notes', '')
            
            submission.save()
            submission.tool.save()
            
            return Response(ToolSubmissionSerializer(submission).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
