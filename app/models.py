from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from uuid import uuid4
from time import time

db = SQLAlchemy()
Base = db.Model


class User(Base):
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    mail = Column(String(300), unique=True, nullable=False)
    password_hash = Column(String(512), nullable=False)
    is_confirmed = Column(Boolean, default=False)
