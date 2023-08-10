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
        curl \   
        gnupg \ 
        && apt-get -y autoremove \
        && apt-get clean

# Installation du pilote ODBC pour Azure SQL
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/21.10/prod impish main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

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
