"""URL patterns for the resumes app."""

from django.urls import path
from .views import ResumeUploadView, MyResumeView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('my/', MyResumeView.as_view(), name='my-resume'),
]
