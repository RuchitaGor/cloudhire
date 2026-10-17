"""Serializers for the resumes app."""

from rest_framework import serializers
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume objects."""

    class Meta:
        model = Resume
        fields = ('id', 'candidate', 'cloudinary_url', 'original_filename', 'uploaded_at')
        read_only_fields = ('id', 'candidate', 'cloudinary_url', 'original_filename', 'uploaded_at')


class ResumeUploadSerializer(serializers.Serializer):
    """Serializer for accepting resume file uploads."""

    file = serializers.FileField()

    def validate_file(self, value):
        filename = value.name.lower()
        if not (filename.endswith('.pdf') or filename.endswith('.docx') or filename.endswith('.txt')):
            raise serializers.ValidationError('Only PDF, DOCX, and TXT files are allowed.')
        max_size = 5 * 1024 * 1024  # 5 MB
        if value.size > max_size:
            raise serializers.ValidationError('File size must be under 5 MB.')
        return value
