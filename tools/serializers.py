from rest_framework import serializers
from .models import Tool, Language
from categories.serializers import CategorySerializer
from categories.models import Category


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'slug', 'icon']

class ToolListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Tool
        fields = ['id', 'name', 'slug', 'short_description', 'github_url', 'logo', 
                  'categories', 'languages', 'creator_username', 'stars_count', 
                  'average_rating', 'views_count', 'last_updated', 'created_at']

class ToolDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tool
        fields = ['id', 'name', 'slug', 'description', 'short_description', 'github_url', 
                  'website_url', 'logo', 'categories', 'languages', 'creator', 'status',
                  'views_count', 'downloads_count', 'stars_count', 'average_rating', 
                  'is_featured', 'last_updated', 'created_at']
        read_only_fields = ['id', 'slug', 'status', 'views_count', 'downloads_count', 
                           'stars_count', 'average_rating', 'created_at', 'last_updated']

class ToolCreateSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        many=True, 
        source='categories',
        write_only=True
    )
    language_ids = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), 
        many=True, 
        source='languages',
        write_only=True
    )

    class Meta:
        model = Tool
        fields = ['name', 'description', 'short_description', 'github_url', 'website_url', 
                  'logo', 'category_ids', 'language_ids']

    def create(self, validated_data):
        return Tool.objects.create(**validated_data)