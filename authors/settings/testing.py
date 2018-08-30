from authors.settings.base import *
import os

# override base.py here

DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES['default']['NAME'] = os.environ.get("DATABASE_TEST_NAME")

