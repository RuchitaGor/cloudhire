"""Views for the resumes app."""

import os
import cloudinary
import cloudinary.uploader
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import IsCandidate
from .models import Resume
from .serializers import ResumeSerializer, ResumeUploadSerializer


def _is_cloudinary_configured():
    """Return True if real Cloudinary credentials are set."""
    cloud = getattr(settings, 'CLOUDINARY_STORAGE', {})
    name = cloud.get('CLOUD_NAME', '')
    return bool(name) and name != 'placeholder'


class ResumeUploadView(APIView):
    """Candidate: upload a PDF/DOCX resume — Cloudinary or local fallback."""

    permission_classes = [IsCandidate]

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data['file']
        original_filename = uploaded_file.name

        if _is_cloudinary_configured():
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                uploaded_file,
                resource_type='raw',
                folder='cloudhire/resumes',
                public_id=f'resume_{request.user.id}',
                overwrite=True,
            )
            cloudinary_url = upload_result.get('secure_url', '')
        else:
            # Local fallback — save to media/resumes/
            media_dir = os.path.join(settings.BASE_DIR, 'media', 'resumes')
            os.makedirs(media_dir, exist_ok=True)
            ext = os.path.splitext(original_filename)[1]
            local_filename = f'resume_{request.user.id}{ext}'
            local_path = os.path.join(media_dir, local_filename)
            with open(local_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            cloudinary_url = f'http://localhost:8000/media/resumes/{local_filename}'

        # Upsert Resume record
        resume, _ = Resume.objects.update_or_create(
            candidate=request.user,
            defaults={
                'cloudinary_url': cloudinary_url,
                'original_filename': original_filename,
            },
        )

        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)


class MyResumeView(APIView):
    """Candidate: retrieve own resume info."""

    permission_classes = [IsCandidate]

    def get(self, request):
        try:
            resume = Resume.objects.get(candidate=request.user)
        except Resume.DoesNotExist:
            return Response({'detail': 'No resume uploaded yet.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ResumeSerializer(resume).data)

