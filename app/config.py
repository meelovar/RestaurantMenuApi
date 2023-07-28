import os

from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.environ.get("POSTGRES_HOST")
PG_USER = os.environ.get("POSTGRES_USER")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
PG_DB = os.environ.get("POSTGRES_DB")
PG_PORT = os.environ.get("POSTGRES_PORT")
