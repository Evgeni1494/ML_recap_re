
# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
        && apt-get -y autoremove \
        && apt-get clean

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files to working directory
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Start server
CMD ["gunicorn", "ml_app.wsgi:application", "--bind", "0.0.0.0:8000"]
