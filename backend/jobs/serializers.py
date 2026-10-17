"""Serializers for the jobs app."""

from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """Full Job serializer."""

    recruiter_name = serializers.CharField(source='recruiter.full_name', read_only=True)
    recruiter_email = serializers.CharField(source='recruiter.email', read_only=True)

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'description', 'requirements',
            'skills_required', 'location', 'status',
            'recruiter', 'recruiter_name', 'recruiter_email',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'recruiter', 'recruiter_name', 'recruiter_email', 'created_at', 'updated_at')
