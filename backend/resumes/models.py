"""Resume model for the resumes app."""

from django.db import models
from django.conf import settings


class Resume(models.Model):
    """A resume uploaded by a candidate, stored on Cloudinary."""

    candidate = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resume',
        limit_choices_to={'role': 'candidate'},
    )
    file = models.FileField(upload_to='resumes/', blank=True, null=True)
    cloudinary_url = models.URLField(max_length=500, blank=True)
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resumes'

    def __str__(self):
        return f'Resume of {self.candidate.email}'
