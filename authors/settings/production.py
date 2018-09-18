import os

import dj_database_url

from authors.settings import DATABASES

db_env = dj_database_url.config(default=os.environ.get("DATABASE_URL", None), conn_max_age=600)

DATABASES['default'].update(db_env)

DEBUG = True

ALLOWED_HOSTS = ['ah-backend-staging.herokuapp.com', 'ah-backend-production.herokuapp.com']
