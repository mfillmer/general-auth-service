import click
from flask.cli import with_appcontext
from app.models import db
from app.models import User, db, Role, RoleOnUser
from werkzeug.security import generate_password_hash
from uuid import uuid4


@click.command('init-db')
@with_appcontext
def init_db():

    print('drop all tables')
    db.drop_all()

    print('create all tables')
    db.create_all()


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
