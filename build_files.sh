#!/bin/bash

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Reset and create database tables
python3.12 manage.py reset_db

# Collect static files
python3.12 manage.py collectstatic --noinput --clear