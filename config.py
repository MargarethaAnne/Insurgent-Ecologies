"""App configuration."""
from os import environ, path

from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")
    TOP_LEVEL_DIR = environ.get("TOP_LEVEL_DIR")
    UPLOADED_IMAGES_URL = environ.get("UPLOADED_IMAGES_URL")
    UPLOADED_IMAGES_DEST = environ.get("UPLOADED_IMAGES_DEST")
    IMAGES = environ.get("IMAGES")
    
    # RECAPTCHA_PUBLIC_KEY = "iubhiukfgjbkhfvgkdfm"
    # RECAPTCHA_PRIVATE_KEY = "dfjgeiajhrihiughadb"
    # RECAPTCHA_PARAMETERS = {'size': '100%'}

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"