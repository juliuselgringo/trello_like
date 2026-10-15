# projects_app/tests/conftest.py
import pytest
from django.conf import settings

def pytest_configure():
    """Force SQLite pour TOUS les tests."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }