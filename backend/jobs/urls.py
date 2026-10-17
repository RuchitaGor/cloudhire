"""URL patterns for the jobs app."""

from django.urls import path
from .views import (
    PublicJobListView,
    PublicJobDetailView,
    RecruiterJobListCreateView,
    RecruiterJobDetailView,
)

urlpatterns = [
    # Public endpoints
    path('', PublicJobListView.as_view(), name='public-job-list'),
    path('<int:pk>/', PublicJobDetailView.as_view(), name='public-job-detail'),

    # Recruiter endpoints
    path('manage/', RecruiterJobListCreateView.as_view(), name='recruiter-job-list-create'),
    path('manage/<int:pk>/', RecruiterJobDetailView.as_view(), name='recruiter-job-detail'),
]
