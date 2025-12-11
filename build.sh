#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set Python path to current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate