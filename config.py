import os
from datetime import timedelta

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'refreshlabs.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TUTORIALS_DIR = os.path.join(BASE_DIR, "app", "content", "tutorials")

    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme-refreshlabs")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Set SESSION_COOKIE_SECURE=1 in production (requires HTTPS); left off by
    # default so local dev over plain http still gets a session cookie.
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
    YOUTUBE_CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")
