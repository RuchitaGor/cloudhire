"""Serializers for the applications app."""

from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    """Full application serializer with nested candidate and job info."""

    candidate_name = serializers.CharField(source='candidate.full_name', read_only=True)
    candidate_email = serializers.CharField(source='candidate.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_id = serializers.IntegerField(source='job.id', read_only=True)
    resume_url = serializers.SerializerMethodField()
    resume_filename = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = (
            'id', 'candidate', 'candidate_name', 'candidate_email',
            'job', 'job_title', 'job_id',
            'resume', 'resume_url', 'resume_filename',
            'status', 'match_score', 'applied_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'candidate', 'candidate_name', 'candidate_email',
            'job', 'job_title', 'job_id',
            'resume', 'resume_url', 'resume_filename',
            'match_score', 'applied_at', 'updated_at',
        )

    def get_resume_url(self, obj):
        if obj.resume:
            return obj.resume.cloudinary_url
        return None

    def get_resume_filename(self, obj):
        if obj.resume:
            return obj.resume.original_filename
        return None


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """Serializer for recruiter status updates only."""

    class Meta:
        model = Application
        fields = ('id', 'status',)
