from django.contrib import admin
from .models import Tool, Language

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'creator', 'stars_count', 'views_count', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at', 'categories', 'languages']
    search_fields = ['name', 'description', 'creator__username']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views_count', 'downloads_count', 'stars_count', 'average_rating', 'created_at', 'last_updated']
    filter_horizontal = ['categories', 'languages']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'description', 'short_description')}),
        ('URLs', {'fields': ('github_url', 'website_url')}),
        ('Media', {'fields': ('logo',)}),
        ('Classification', {'fields': ('categories', 'languages')}),
        ('Creator', {'fields': ('creator',)}),
        ('Status', {'fields': ('status', 'is_featured')}),
        ('Stats', {'fields': ('views_count', 'downloads_count', 'stars_count', 'average_rating')}),
        ('Timestamps', {'fields': ('created_at', 'last_updated')}),
    )