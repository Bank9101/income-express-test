#!/bin/bash

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Run migrations
python3.12 manage.py migrate --noinput

# Run syncdb to ensure all tables are created
python3.12 manage.py migrate --run-syncdb --noinput

# Setup default categories if not exists
python3.12 manage.py setup_categories

# Collect static files
python3.12 manage.py collectstatic --noinput --clear