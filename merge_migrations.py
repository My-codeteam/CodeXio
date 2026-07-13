#!/usr/bin/env python
import os
import sys
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codexio.settings")
django.setup()

try:
    call_command('makemigrations', '--merge', '--noinput')
    print("Migrations merged successfully!")
except Exception as e:
    print(f"Error during merge: {e}")
    sys.exit(1)
