import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:example@localhost:5432/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ["APP_SECRET_KEY"]