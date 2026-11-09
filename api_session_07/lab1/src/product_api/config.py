import os

class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
