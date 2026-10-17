"""Admin registration for the jobs app."""

from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'status', 'location', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'skills_required')
    ordering = ('-created_at',)
