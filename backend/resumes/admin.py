"""Admin registration for the resumes app."""

from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'original_filename', 'uploaded_at')
    search_fields = ('candidate__email',)
