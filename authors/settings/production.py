import os

import dj_database_url

db_env = dj_database_url.config(default=os.environ.get("DATABASE_URL", None), conn_max_age=600)

DEBUG = False

ALLOWED_HOSTS = ['ah-backend-staging.herokuapp.com', 'ah-backend-production.herokuapp.com']
