"""Admin registration for the applications app."""

from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'match_score', 'applied_at')
    list_filter = ('status',)
    search_fields = ('candidate__email', 'job__title')
    ordering = ('-match_score', '-applied_at')
