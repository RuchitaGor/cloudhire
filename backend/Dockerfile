# ─── Backend Dockerfile ───────────────────────────────────────────────────────
FROM python:3.11-slim

# System deps for PyMuPDF
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Start gunicorn
CMD ["gunicorn", "cloudhire_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
