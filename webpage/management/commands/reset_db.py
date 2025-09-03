from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Reset and create database tables for Vercel deployment'

    def handle(self, *args, **options):
        try:
            # Get current database connection
            with connection.cursor() as cursor:
                self.stdout.write('Checking database connection...')
                
                # Check if we're using PostgreSQL
                if connection.vendor == 'postgresql':
                    self.stdout.write('PostgreSQL detected. Creating tables manually...')
                    
                    # Drop tables if they exist (be careful!)
                    tables_to_drop = [
                        'webpage_transaction',
                        'webpage_budget', 
                        'webpage_category'
                    ]
                    
                    for table in tables_to_drop:
                        try:
                            cursor.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')
                            self.stdout.write(f'Dropped table: {table}')
                        except Exception as e:
                            self.stdout.write(f'Warning: Could not drop {table}: {e}')
                    
                    # Create tables manually
                    self.stdout.write('Creating tables manually...')
                    
                    # Create webpage_category table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS webpage_category (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            type VARCHAR(10) NOT NULL,
                            color VARCHAR(7) DEFAULT '#007bff',
                            icon VARCHAR(50) DEFAULT 'fas fa-tag'
                        );
                    """)
                    
                    # Create webpage_transaction table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS webpage_transaction (
                            id SERIAL PRIMARY KEY,
                            amount DECIMAL(10, 2) NOT NULL,
                            description TEXT,
                            date DATE DEFAULT CURRENT_DATE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            user_id INTEGER NOT NULL,
                            category_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES auth_user(id),
                            FOREIGN KEY (category_id) REFERENCES webpage_category(id)
                        );
                    """)
                    
                    # Create webpage_budget table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS webpage_budget (
                            id SERIAL PRIMARY KEY,
                            amount DECIMAL(10, 2) NOT NULL,
                            month DATE NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            user_id INTEGER NOT NULL,
                            category_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES auth_user(id),
                            FOREIGN KEY (category_id) REFERENCES webpage_category(id),
                            UNIQUE (user_id, category_id, month)
                        );
                    """)
                    
                    self.stdout.write('Tables created successfully!')
                    
                    # Setup categories
                    self.stdout.write('Setting up categories...')
                    call_command('setup_categories')
                    
                    self.stdout.write(self.style.SUCCESS('Database reset complete!'))
                    
                else:
                    # For SQLite, just run migrations
                    self.stdout.write('SQLite detected. Running standard migrations...')
                    call_command('migrate', verbosity=2)
                    call_command('setup_categories')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during database reset: {e}')
            )