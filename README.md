# ☁ CloudHire — AI-Based Recruitment & Resume Screening Portal

A full-stack cloud-based recruitment platform that uses an AI-powered skill matching engine to assist recruiters in screening candidates efficiently.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Setup (Manual)](#local-setup-manual)
- [Local Setup (Docker Compose)](#local-setup-docker-compose)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Deployment (Render)](#deployment-render)
- [CI/CD Pipeline](#cicd-pipeline)

---

## Features

| Role | Features |
|---|---|
| **Candidate** | Register/Login, Search Jobs, Upload Resume (PDF/DOCX), Apply for Jobs, Track Application Status |
| **Recruiter** | Register/Login, Post/Edit/Archive Jobs, View Applicants, AI Skill Match Scores, Shortlist/Reject |
| **Admin** | Manage Users (List/Delete), View System Reports |

### AI Skill Matching Engine
- Downloads resume from Cloudinary
- Extracts text from PDF (PyMuPDF) or DOCX (python-docx)
- Tokenizes and compares skills against job requirements
- Calculates a **match percentage (0–100%)** stored with each application

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js (Vite), React Router, Axios |
| Backend | Django 4.2, Django REST Framework, SimpleJWT |
| Database | MySQL 8 |
| Cloud Storage | Cloudinary |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Render |
| Version Control | Git / GitHub |

---

## Architecture

```
Frontend (React.js / Vite)
        ↓
Django REST API (DRF + SimpleJWT)
        ↓
AI Skill Matching Engine (PyMuPDF + python-docx)
        ↓
MySQL 8 Database
        ↓
Cloudinary Storage (resumes)
```

**Deployment Pipeline:**
```
GitHub Repository → GitHub Actions → Docker Images → Render Cloud
```

---

## Project Structure

```
cloudhire/
├── backend/
│   ├── cloudhire_project/       # Django project config (settings, urls, wsgi)
│   ├── users/                   # CustomUser model, auth endpoints, permissions
│   ├── jobs/                    # Job model, recruiter CRUD, public search
│   ├── resumes/                 # Resume model, Cloudinary upload
│   ├── applications/            # Application model, AI matcher, status updates
│   │   └── ai_matcher.py        # AI Skill Matching Engine
│   ├── requirements.txt
│   ├── Dockerfile
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── api/axios.js         # Axios client + all API functions
│   │   ├── context/             # AuthContext (JWT + user role)
│   │   ├── components/          # Navbar, ProtectedRoute
│   │   └── pages/               # All role-specific pages
│   ├── nginx.conf               # Nginx SPA config
│   ├── Dockerfile
│   └── package.json
├── .github/workflows/deploy.yml # GitHub Actions CI/CD
├── docker-compose.yml
├── render.yaml
└── README.md
```

---

## Prerequisites

- Python 3.11+
- Node.js 20+
- MySQL 8
- Docker & Docker Compose (for containerized setup)
- A [Cloudinary](https://cloudinary.com/) account (free tier works)

---

## Local Setup (Manual)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cloudhire.git
cd cloudhire
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a MySQL database
mysql -u root -p
# In MySQL:
CREATE DATABASE cloudhire_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'cloudhire_user'@'localhost' IDENTIFIED BY 'cloudhire_password';
GRANT ALL PRIVILEGES ON cloudhire_db.* TO 'cloudhire_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Configure environment
cp .env.example .env
# Edit .env with your MySQL and Cloudinary credentials

# Apply migrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Backend will be running at: **http://localhost:8000**

### 3. Frontend Setup

```bash
cd frontend

# Configure environment
cp .env.example .env
# .env should contain: VITE_API_URL=http://localhost:8000/api

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be running at: **http://localhost:5173**

---

## Local Setup (Docker Compose)

> Requires Docker Desktop or Docker Engine + Compose.

### 1. Configure Backend Environment

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your Cloudinary credentials.
# DB_HOST must be: db (the Docker service name)
```

### 2. Start All Services

```bash
docker compose up --build
```

This starts:
- **MySQL** on port 3306
- **Django backend** on port 8000 (runs migrations automatically)
- **React frontend** on port 3000

Visit: **http://localhost:3000**

### 3. Create Admin User in Docker

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DB_NAME` | MySQL database name | `cloudhire_db` |
| `DB_USER` | MySQL username | `cloudhire_user` |
| `DB_PASSWORD` | MySQL password | `cloudhire_password` |
| `DB_HOST` | MySQL host | `localhost` or `db` (Docker) |
| `DB_PORT` | MySQL port | `3306` |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name | `my-cloud` |
| `CLOUDINARY_API_KEY` | Cloudinary API key | `123456789` |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | `abc123secret` |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |

### Frontend (`frontend/.env`)

| Variable | Description | Example |
|---|---|---|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000/api` |

---

## API Endpoints

### Authentication (`/api/auth/`)
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/register/` | Register user | Public |
| POST | `/login/` | Login, returns JWT | Public |
| POST | `/token/refresh/` | Refresh JWT | Public |
| GET | `/me/` | Get own profile | JWT |
| GET | `/admin/users/` | List all users | Admin |
| DELETE | `/admin/users/<id>/` | Delete user | Admin |

### Jobs (`/api/jobs/`)
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/` | List published jobs | Public |
| GET | `/<id>/` | Get job details | Public |
| GET | `/manage/` | Recruiter's own jobs | Recruiter |
| POST | `/manage/` | Create job | Recruiter |
| PATCH | `/manage/<id>/` | Update job | Recruiter |
| DELETE | `/manage/<id>/` | Delete job | Recruiter |

### Resumes (`/api/resumes/`)
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/upload/` | Upload PDF/DOCX to Cloudinary | Candidate |
| GET | `/my/` | Get own resume | Candidate |

### Applications (`/api/applications/`)
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/apply/<job_id>/` | Apply for job (runs AI match) | Candidate |
| GET | `/my/` | List own applications | Candidate |
| GET | `/job/<job_id>/` | List applicants for job | Recruiter |
| PATCH | `/<id>/status/` | Update application status | Recruiter |
| GET | `/report/` | All applications report | Admin |

---

## Deployment (Render)

### Prerequisites
1. A [Render](https://render.com) account
2. A Docker Hub account
3. Cloudinary credentials

### Steps

1. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/your-username/cloudhire.git
   git push -u origin main
   ```

2. **Set GitHub Secrets** (Settings → Secrets → Actions):
   - `DOCKER_HUB_USERNAME`
   - `DOCKER_HUB_TOKEN`
   - `RENDER_API_KEY`
   - `RENDER_BACKEND_SERVICE_ID`
   - `RENDER_FRONTEND_SERVICE_ID`
   - `VITE_API_URL`

3. **Deploy on Render:**
   - Connect your GitHub repo to Render
   - Render auto-detects `render.yaml`
   - Set Cloudinary env vars in the Render dashboard

---

## CI/CD Pipeline

On every push to `main`, GitHub Actions:

1. **Tests Django backend** — runs `python manage.py test` with a MySQL service
2. **Builds React frontend** — runs `npm run build`
3. **Builds & pushes Docker images** to Docker Hub
4. **Deploys to Render** via Render Deploy Hook API

See [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) for full details.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
