"""
CI/Testing environment settings
"""
from .base import *
import os

# CI Database configuration
if os.environ.get('GITHUB_ACTIONS'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DATABASE_NAME', 'test_teleconsult'),
            'USER': os.environ.get('DATABASE_USER', 'root'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'root'),
            'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DATABASE_PORT', '3306'),
        }
    }
else:
    # Local testing with SQLite for speed
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Disable migrations for faster testing
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

# Only disable migrations in non-CI environments to speed up local testing
if not os.environ.get('GITHUB_ACTIONS'):
    MIGRATION_MODULES = DisableMigrations()
