import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "madeuppassword"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In-memory database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
