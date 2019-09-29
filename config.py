import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GITHUB_OAUTH_CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID")
    GITHUB_OAUTH_CLIENT_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET")
