"""Job model for the jobs app."""

from django.db import models
from django.conf import settings


class Job(models.Model):
    """A job posting created by a recruiter."""

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'recruiter'},
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(help_text='General job requirements.')
    skills_required = models.TextField(
        help_text='Comma-separated list of required skills, e.g. Python,Django,REST'
    )
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} [{self.status}]'

    def get_skills_list(self):
        """Return skills as a cleaned list."""
        return [s.strip().lower() for s in self.skills_required.split(',') if s.strip()]
