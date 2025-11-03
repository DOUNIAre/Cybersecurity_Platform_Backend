from rest_framework import serializers
from .models import ToolSubmission
from tools.serializers import ToolDetailSerializer

class ToolSubmissionSerializer(serializers.ModelSerializer):
    tool = ToolDetailSerializer(read_only=True)
    submitter_username = serializers.CharField(source='submitter.username', read_only=True)

    class Meta:
        model = ToolSubmission
        fields = ['id', 'tool', 'submitter_username', 'status', 'review_notes', 
                  'created_at', 'updated_at', 'reviewed_at']
        read_only_fields = ['id', 'submitter_username', 'status', 'review_notes', 
                           'created_at', 'updated_at', 'reviewed_at']

class ToolSubmissionCreateSerializer(serializers.Serializer):
    tool_name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    short_description = serializers.CharField(max_length=500)
    github_url = serializers.URLField()
    website_url = serializers.URLField(required=False, allow_blank=True)
    category_ids = serializers.ListField(child=serializers.IntegerField())
    language_ids = serializers.ListField(child=serializers.IntegerField())
    logo = serializers.ImageField(required=False)

class ToolSubmissionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolSubmission
        fields = ['status', 'review_notes']