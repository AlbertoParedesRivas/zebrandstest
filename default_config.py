import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:example@postgres:5432/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SECRET_KEY = os.environ["APP_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = True
# JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]