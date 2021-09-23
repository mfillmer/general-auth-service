from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from uuid import uuid4
from time import time

db = SQLAlchemy()
Base = db.Model


class Request(Base):
    __tablename__ = 'requests'
    uuid = Column(String(36), primary_key=True, default=lambda: uuid4())
    timestamp = Column(BIGINT, default=lambda: str(int(time()*1000)))
