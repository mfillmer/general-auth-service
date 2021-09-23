import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI') or 'sqlite:///data/db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
    'SQLALCHEMY_TRACK_MODIFICATIONS') or False
