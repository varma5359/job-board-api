"""
Admin configuration for the jobs app.
"""

from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin view for Job model."""
    list_display = ('title', 'company', 'location', 'recruiter', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('title', 'company', 'location')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin view for Application model."""
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'job__title')