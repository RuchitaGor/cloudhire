"""Views for the applications app."""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

from jobs.models import Job
from resumes.models import Resume
from users.permissions import IsCandidate, IsRecruiter
from .models import Application
from .serializers import ApplicationSerializer, ApplicationStatusSerializer
from .ai_matcher import run_skill_matching


class ApplyForJobView(APIView):
    """Candidate: apply for a published job. Triggers AI skill matching."""

    permission_classes = [IsCandidate]

    def post(self, request, job_id):
        # Validate job exists and is published
        try:
            job = Job.objects.get(pk=job_id, status='published')
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found or not published.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure candidate has uploaded a resume
        try:
            resume = Resume.objects.get(candidate=request.user)
        except Resume.DoesNotExist:
            return Response({'detail': 'Please upload your resume before applying.'}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicate applications
        if Application.objects.filter(candidate=request.user, job=job).exists():
            raise ValidationError('You have already applied for this job.')

        # Run AI skill matching engine
        ai_result = run_skill_matching(
            cloudinary_url=resume.cloudinary_url,
            original_filename=resume.original_filename,
            skills_required=job.skills_required,
        )

        # Create application with match score
        application = Application.objects.create(
            candidate=request.user,
            job=job,
            resume=resume,
            match_score=ai_result['match_score'],
            status='pending',
        )

        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


class CandidateApplicationListView(generics.ListAPIView):
    """Candidate: list own applications."""

    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user).order_by('-applied_at')


class RecruiterApplicantsView(generics.ListAPIView):
    """Recruiter: list all applicants for one of their jobs."""

    serializer_class = ApplicationSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        # Ensure job belongs to this recruiter
        try:
            job = Job.objects.get(pk=job_id, recruiter=self.request.user)
        except Job.DoesNotExist:
            raise PermissionDenied('Job not found or not yours.')
        return Application.objects.filter(job=job).order_by('-match_score', '-applied_at')


class UpdateApplicationStatusView(generics.UpdateAPIView):
    """Recruiter: shortlist or reject a candidate application."""

    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsRecruiter]
    http_method_names = ['patch']

    def get_queryset(self):
        return Application.objects.filter(job__recruiter=self.request.user)

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ('shortlisted', 'rejected', 'pending'):
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        application.status = new_status
        application.save()
        return Response(ApplicationSerializer(application).data)


class AdminApplicationReportView(generics.ListAPIView):
    """Admin: view all applications (system report)."""

    from users.permissions import IsAdmin
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Application.objects.all().order_by('-applied_at')
