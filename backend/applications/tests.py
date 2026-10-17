"""Unit tests for the AI skill matching engine."""

from django.test import TestCase
from .ai_matcher import calculate_match_score, _tokenize, _normalize_skill


class AIMatcherTests(TestCase):

    def test_perfect_match(self):
        resume = "Python Django REST API MySQL Docker"
        skills = "Python,Django,MySQL"
        score = calculate_match_score(resume, skills)
        self.assertEqual(score, 100.0)

    def test_partial_match(self):
        resume = "Python Flask SQL"
        skills = "Python,Django,MySQL"
        score = calculate_match_score(resume, skills)
        # Only "Python" matches → 1/3 = 33.33%
        self.assertAlmostEqual(score, 33.33, places=1)

    def test_no_match(self):
        resume = "Java Spring Hibernate"
        skills = "Python,Django,MySQL"
        score = calculate_match_score(resume, skills)
        self.assertEqual(score, 0.0)

    def test_empty_resume(self):
        score = calculate_match_score('', 'Python,Django')
        self.assertEqual(score, 0.0)

    def test_empty_skills(self):
        score = calculate_match_score('Python Django', '')
        self.assertEqual(score, 0.0)

    def test_case_insensitive(self):
        resume = "PYTHON django REST api"
        skills = "Python,Django,REST"
        score = calculate_match_score(resume, skills)
        self.assertEqual(score, 100.0)

    def test_score_range(self):
        resume = "React JavaScript"
        skills = "React,JavaScript,Node.js"
        score = calculate_match_score(resume, skills)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_tokenize(self):
        tokens = _tokenize("Python 3.9, Django REST")
        self.assertIn('python', tokens)
        self.assertIn('django', tokens)
        self.assertIn('rest', tokens)
