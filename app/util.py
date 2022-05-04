import click
from flask.cli import with_appcontext
from flask_jwt_extended.utils import create_access_token
from app.models import db
from app.models import User, db, Role, RoleOnUser
from werkzeug.security import generate_password_hash
from uuid import uuid4


@click.command('init-db')
@with_appcontext
def init_db():
    '''Recreate database completly.'''
    print('drop all tables')
    db.drop_all()

    print('create all tables')
    db.create_all()


def update_users_password(mail, password):
    user = User.query.filter_by(mail=mail).first()
    pw_hash = generate_password_hash(password)
    user.password_hash = pw_hash
    db.session.commit()


def delete_user_by_mail(mail):
    User.query.filter_by(mail=mail).delete()
    db.session.commit()


def create_user(mail, alias, password):
    pw_hash = generate_password_hash(password)
    user_uuid = str(uuid4())
    user = User(uuid=user_uuid, alias=alias,
                mail=mail, password_hash=pw_hash)
    default_role = Role.query.filter_by(is_default=True).first()
    db.session.add(user)
    if default_role is not None:
        role_on_user = RoleOnUser(
            user_uuid=user_uuid, role_name=default_role.name)
        db.session.add(role_on_user)
    db.session.commit()

    return user


def flatten(t):
    return list(set([item for sublist in t for item in sublist]))


def get_user_access_token(user: User):
    permissions = list(map(lambda p: p.name, flatten(user.permissions)))
    alias = user.alias

    return create_access_token(user.uuid, additional_claims=dict(permissions=permissions, alias=alias))
