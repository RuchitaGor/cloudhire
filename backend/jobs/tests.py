"""Unit tests for the jobs app."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Job

User = get_user_model()


class JobModelTests(TestCase):

    def setUp(self):
        self.recruiter = User.objects.create_user(
            email='recruiter@test.com',
            password='testpass123',
            full_name='Recruiter One',
            role='recruiter',
        )

    def test_create_job(self):
        job = Job.objects.create(
            recruiter=self.recruiter,
            title='Python Developer',
            description='Build backend APIs',
            requirements='3+ years experience',
            skills_required='Python,Django,MySQL',
            status='published',
        )
        self.assertEqual(job.title, 'Python Developer')
        self.assertEqual(job.status, 'published')

    def test_get_skills_list(self):
        job = Job.objects.create(
            recruiter=self.recruiter,
            title='Test Job',
            description='Desc',
            requirements='Req',
            skills_required='  Python , Django , REST API ',
        )
        skills = job.get_skills_list()
        self.assertIn('python', skills)
        self.assertIn('django', skills)
        self.assertIn('rest api', skills)

    def test_default_status_is_draft(self):
        job = Job.objects.create(
            recruiter=self.recruiter,
            title='Draft Job',
            description='Desc',
            requirements='Req',
            skills_required='Python',
        )
        self.assertEqual(job.status, 'draft')
