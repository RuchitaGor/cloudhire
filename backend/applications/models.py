"""Application model for the applications app."""

from django.db import models
from django.conf import settings
from jobs.models import Job
from resumes.models import Resume


class Application(models.Model):
    """A candidate's application for a job."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': 'candidate'},
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    match_score = models.FloatField(default=0.0)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'
        unique_together = ('candidate', 'job')
        ordering = ['-match_score', '-applied_at']

    def __str__(self):
        return f'{self.candidate.email} → {self.job.title} [{self.status}]'
