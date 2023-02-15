#!/bin/bash

# Run db migrations
python manage.py migrate

# Running development server
gunicorn -c gunicorn_config.py admin_settings.wsgi -b 0.0.0.0:8000
