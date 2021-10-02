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
    timestamp = Column(BigInteger, default=lambda: str(int(time()*1000)))
    is_confirmed = Column(Boolean, default=False)


class RevokedToken(Base):
    jti = Column(String(36), primary_key=True)


class Permission(Base):
    name = Column(String(300), primary_key=True)


class Role(Base):
    name = Column(String(300), primary_key=True)
