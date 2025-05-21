# tutorT/config.py
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env')) # Load environment variables from .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # CHANGE THIS!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db') # MODIFIED LINE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other configurations here later