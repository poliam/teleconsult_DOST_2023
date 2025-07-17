"""
Test settings that use SQLite instead of MySQL for testing
"""
from Teleconsult.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use in-memory database for tests
    }
}
# python manage.py test patient.test_gps_crud patient.test_gps_validations -v 2