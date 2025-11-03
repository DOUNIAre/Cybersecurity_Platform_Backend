from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'tools_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'tools_count', 'created_at', 'updated_at']