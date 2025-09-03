#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webappincome.settings')
django.setup()

from django.db import connection

def check_tables():
    with connection.cursor() as cursor:
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name LIKE 'webpage_%'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print("Found webpage tables:", tables)
        
        # Check if specific table exists
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'webpage_transaction'
        """)
        result = cursor.fetchone()
        print(f"webpage_transaction exists: {result is not None}")
        
        if not result:
            print("Transaction table not found. Need to create it.")
            return False
        return True

if __name__ == "__main__":
    try:
        exists = check_tables()
        if not exists:
            print("Running migrations...")
            os.system("python manage.py migrate --run-syncdb")
    except Exception as e:
        print(f"Error: {e}")