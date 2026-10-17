"""URL patterns for the applications app."""

from django.urls import path
from .views import (
    ApplyForJobView,
    CandidateApplicationListView,
    RecruiterApplicantsView,
    UpdateApplicationStatusView,
    AdminApplicationReportView,
)

urlpatterns = [
    # Candidate
    path('apply/<int:job_id>/', ApplyForJobView.as_view(), name='apply-for-job'),
    path('my/', CandidateApplicationListView.as_view(), name='candidate-applications'),

    # Recruiter
    path('job/<int:job_id>/', RecruiterApplicantsView.as_view(), name='recruiter-applicants'),
    path('<int:pk>/status/', UpdateApplicationStatusView.as_view(), name='update-application-status'),

    # Admin
    path('report/', AdminApplicationReportView.as_view(), name='admin-report'),
]
