from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import *
from uuid import uuid4
from time import time

from sqlalchemy.orm import relationship

db = SQLAlchemy()
Base = db.Model


class User(Base):
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    mail = Column(String(300), unique=True, nullable=False)
    password_hash = Column(String(512), nullable=False)
    timestamp = Column(BigInteger, default=lambda: str(int(time()*1000)))
    is_confirmed = Column(Boolean, default=False)
    role = relationship('Role')
    role_name = Column(String(300), ForeignKey(
        'role.name'), default=lambda: Role.get_default())
    permissions = association_proxy('role', 'permission')


class RevokedToken(Base):
    jti = Column(String(36), primary_key=True)


class Permission(Base):
    name = Column(String(300), primary_key=True)


class Role(Base):
    name = Column(String(300), primary_key=True)
    perms = relationship('PermissionOnRole', uselist=True)
    permissions = association_proxy('perms', 'permission')
    is_default = Column(Boolean, default=False)
    users = relationship('User', uselist=True)

    def get_default():
        default = Role.query.filter_by(is_default=True).first()
        if default is not None:
            return default.name
        return ''


class PermissionOnRole(Base):
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    role = Column(String(300), ForeignKey('role.name'))
    perm = Column(String(300), ForeignKey('permission.name'))
    permission = relationship('Permission')
