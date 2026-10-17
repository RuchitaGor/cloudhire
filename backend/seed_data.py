"""Seed sample data: recruiter + 5 published jobs."""
import os
import sys
import django

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudhire_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

# Create recruiter
if not User.objects.filter(email='recruiter@cloudhire.com').exists():
    recruiter = User.objects.create_user(
        email='recruiter@cloudhire.com',
        password='Recruiter@123',
        full_name='TechCorp HR',
        role='recruiter',
    )
    print('[OK] Recruiter created: recruiter@cloudhire.com / Recruiter@123')
else:
    recruiter = User.objects.get(email='recruiter@cloudhire.com')
    print('[--] Recruiter already exists')

jobs_data = [
    {
        'title': 'Python Backend Developer',
        'description': 'We are looking for an experienced Python developer to join our growing team. You will design and build scalable REST APIs and work closely with the frontend team.',
        'requirements': '3+ years Python experience. Strong knowledge of Django or Flask. Experience with REST APIs and databases.',
        'skills_required': 'Python,Django,REST API,MySQL,Git',
        'location': 'Bangalore, India',
        'status': 'published',
    },
    {
        'title': 'React Frontend Engineer',
        'description': 'Join our product team to build beautiful, responsive web applications. You will work on our customer-facing portal using React and modern JavaScript.',
        'requirements': '2+ years React experience. Proficiency in JavaScript, HTML, CSS. Experience with state management.',
        'skills_required': 'React,JavaScript,HTML,CSS,Git,Redux',
        'location': 'Remote',
        'status': 'published',
    },
    {
        'title': 'Full Stack Developer',
        'description': 'Exciting opportunity to work on both frontend and backend of our SaaS platform. Own features end-to-end and collaborate with design and DevOps teams.',
        'requirements': 'Experience in both frontend and backend development. Knowledge of cloud platforms. Good communication skills.',
        'skills_required': 'Python,Django,React,JavaScript,MySQL,Docker,REST API',
        'location': 'Hyderabad, India',
        'status': 'published',
    },
    {
        'title': 'DevOps Engineer',
        'description': 'Help automate our CI/CD pipelines, manage cloud infrastructure, and ensure high availability of our services.',
        'requirements': '2+ years DevOps experience. Experience with Docker and Kubernetes. Knowledge of AWS or GCP.',
        'skills_required': 'Docker,Kubernetes,AWS,GitHub Actions,Linux,CI/CD,Python',
        'location': 'Pune, India',
        'status': 'published',
    },
    {
        'title': 'Data Analyst',
        'description': 'Analyze large datasets to extract actionable insights. Build dashboards and reports for business stakeholders.',
        'requirements': 'Strong analytical mindset. Proficiency in SQL and Python. Experience with data visualization tools.',
        'skills_required': 'Python,SQL,MySQL,Pandas,Excel,Data Analysis',
        'location': 'Chennai, India',
        'status': 'published',
    },
]

for jd in jobs_data:
    job, created = Job.objects.get_or_create(
        title=jd['title'],
        defaults={**jd, 'recruiter': recruiter}
    )
    status = '[CREATED]' if created else '[EXISTS] '
    print(f'{status} {job.title}')

total = Job.objects.filter(status='published').count()
print(f'\nTotal published jobs: {total}')
print('\nRecruiter login:  recruiter@cloudhire.com  /  Recruiter@123')
print('Admin login:      admin@cloudhire.com      /  Admin@123')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudhire_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

# Create recruiter
if not User.objects.filter(email='recruiter@cloudhire.com').exists():
    recruiter = User.objects.create_user(
        email='recruiter@cloudhire.com',
        password='Recruiter@123',
        full_name='TechCorp HR',
        role='recruiter',
    )
    print('✅ Recruiter created: recruiter@cloudhire.com / Recruiter@123')
else:
    recruiter = User.objects.get(email='recruiter@cloudhire.com')
    print('ℹ  Recruiter already exists')

jobs_data = [
    {
        'title': 'Python Backend Developer',
        'description': 'We are looking for an experienced Python developer to join our growing team. You will design and build scalable REST APIs and work closely with the frontend team.',
        'requirements': '3+ years Python experience. Strong knowledge of Django or Flask. Experience with REST APIs and databases.',
        'skills_required': 'Python,Django,REST API,MySQL,Git',
        'location': 'Bangalore, India',
        'status': 'published',
    },
    {
        'title': 'React Frontend Engineer',
        'description': 'Join our product team to build beautiful, responsive web applications. You will work on our customer-facing portal using React and modern JavaScript.',
        'requirements': '2+ years React experience. Proficiency in JavaScript, HTML, CSS. Experience with state management.',
        'skills_required': 'React,JavaScript,HTML,CSS,Git,Redux',
        'location': 'Remote',
        'status': 'published',
    },
    {
        'title': 'Full Stack Developer',
        'description': 'Exciting opportunity to work on both frontend and backend of our SaaS platform. Own features end-to-end and collaborate with design and DevOps teams.',
        'requirements': 'Experience in both frontend and backend development. Knowledge of cloud platforms. Good communication skills.',
        'skills_required': 'Python,Django,React,JavaScript,MySQL,Docker,REST API',
        'location': 'Hyderabad, India',
        'status': 'published',
    },
    {
        'title': 'DevOps Engineer',
        'description': 'Help automate our CI/CD pipelines, manage cloud infrastructure, and ensure high availability of our services.',
        'requirements': '2+ years DevOps experience. Experience with Docker and Kubernetes. Knowledge of AWS or GCP.',
        'skills_required': 'Docker,Kubernetes,AWS,GitHub Actions,Linux,CI/CD,Python',
        'location': 'Pune, India',
        'status': 'published',
    },
    {
        'title': 'Data Analyst',
        'description': 'Analyze large datasets to extract actionable insights. Build dashboards and reports for business stakeholders.',
        'requirements': 'Strong analytical mindset. Proficiency in SQL and Python. Experience with data visualization tools.',
        'skills_required': 'Python,SQL,MySQL,Pandas,Excel,Data Analysis',
        'location': 'Chennai, India',
        'status': 'published',
    },
]

for jd in jobs_data:
    job, created = Job.objects.get_or_create(
        title=jd['title'],
        defaults={**jd, 'recruiter': recruiter}
    )
    status = '✅ Created' if created else 'ℹ  Exists'
    print(f'{status}: {job.title}')

total = Job.objects.filter(status='published').count()
print(f'\n🎉 Total published jobs: {total}')
print('\nRecruiter login:  recruiter@cloudhire.com  /  Recruiter@123')
print('Admin login:      admin@cloudhire.com      /  Admin@123')
