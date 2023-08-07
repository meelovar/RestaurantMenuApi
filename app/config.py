import os

from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.environ.get('POSTGRES_HOST')
PG_USER = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
PG_DB = os.environ.get('POSTGRES_DB')
PG_PORT = os.environ.get('POSTGRES_PORT')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')

REDIS_HOST_TEST = os.environ.get('REDIS_HOST_TEST')
REDIS_PORT_TEST = os.environ.get('REDIS_PORT_TEST')
