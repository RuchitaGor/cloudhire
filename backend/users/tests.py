"""Unit tests for the users app."""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):

    def test_create_candidate(self):
        user = User.objects.create_user(
            email='candidate@test.com',
            password='testpass123',
            full_name='Test Candidate',
            role='candidate',
        )
        self.assertEqual(user.email, 'candidate@test.com')
        self.assertEqual(user.role, 'candidate')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_recruiter(self):
        user = User.objects.create_user(
            email='recruiter@test.com',
            password='testpass123',
            full_name='Test Recruiter',
            role='recruiter',
        )
        self.assertEqual(user.role, 'recruiter')

    def test_email_is_unique(self):
        User.objects.create_user(email='dup@test.com', password='pass', full_name='A')
        with self.assertRaises(Exception):
            User.objects.create_user(email='dup@test.com', password='pass', full_name='B')
