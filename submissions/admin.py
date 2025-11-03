from django.contrib import admin
from .models import ToolSubmission

@admin.register(ToolSubmission)
class ToolSubmissionAdmin(admin.ModelAdmin):
    list_display = ['tool', 'submitter', 'status', 'reviewer', 'created_at', 'reviewed_at']
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = ['tool__name', 'submitter__username', 'reviewer__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Tool', {'fields': ('tool', 'submitter')}),
        ('Review', {'fields': ('status', 'reviewer', 'review_notes', 'reviewed_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
