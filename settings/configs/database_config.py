import os

ENV = os.environ.get("ENV")

DB_ENGINE = os.environ.get("DB_ENGINE")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = (
    f"{DB_ENGINE}://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

