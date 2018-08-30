from authors.settings.base import *
import dj_database_url
import os

# override base.py here
DEBUG = False
ALLOWED_HOSTS= ['*']
POSTGRES_URL = os.environ.get("DATABASE_URL")

DATABASES['default'] = dj_database_url.parse(POSTGRES_URL, conn_max_age=600)

