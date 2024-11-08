#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
# import json

def main():
    """Run administrative tasks."""
    load_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ciento.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # appUrl = json.loads(os.getenv('API_SETTINGS', '{}'))
    # execute_from_command_line(['manage.py', 'runserver', "127.0.0.1:8000"])
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()