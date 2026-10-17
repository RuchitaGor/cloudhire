"""Views for the jobs app."""

from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied

from .models import Job
from .serializers import JobSerializer
from users.permissions import IsRecruiter


class PublicJobListView(generics.ListAPIView):
    """Public: list all published jobs with optional keyword search."""

    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'skills_required', 'location']

    def get_queryset(self):
        return Job.objects.filter(status='published').order_by('-created_at')


class PublicJobDetailView(generics.RetrieveAPIView):
    """Public: retrieve a single published job."""

    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Job.objects.filter(status='published')


class RecruiterJobListCreateView(generics.ListCreateAPIView):
    """Recruiter: list own jobs or create a new one."""

    serializer_class = JobSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)


class RecruiterJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Recruiter: retrieve, update, or delete own job."""

    serializer_class = JobSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

    def perform_update(self, serializer):
        job = self.get_object()
        if job.recruiter != self.request.user:
            raise PermissionDenied('You do not own this job.')
        serializer.save()
