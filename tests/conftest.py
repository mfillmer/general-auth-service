from flask_jwt_extended.utils import create_access_token
from werkzeug.security import generate_password_hash
from app.models import User, Permission, Role
import pytest
import os

from app import create_app, db as db_instance


@pytest.fixture
def app():
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app = create_app()
    yield app


@pytest.fixture
def db(context):
    with context:
        db_instance.create_all()
        yield db_instance
        db_instance.drop_all()


@pytest.fixture
def context(app):
    yield app.app_context()


@pytest.fixture
def cli_runner(app, db):
    with app.app_context():
        cli_runner = app.test_cli_runner()
        yield cli_runner


@pytest.fixture
def client(app, context, db):
    with app.test_client() as client:
        with context:
            client.context = context
            yield client


@pytest.fixture
def user(context, db):
    with context:
        user = User(mail='user@test.com',
                    password_hash=generate_password_hash('test'))
        db.session.add(user)
        db.session.commit()
        yield user


@pytest.fixture
def permissions(client, db):
    with client.context:
        def to_model(index): return Permission(name=f'test {index}')
        permissions = list(map(to_model, range(5)))
        db.session.add_all(permissions)
        db.session.commit()

        yield permissions


@pytest.fixture
def roles(client, db):
    with client.context:
        def to_model(index): return Role(name=f'test {index}', is_default=True)
        roles = list(map(to_model, range(1)))
        db.session.add_all(roles)
        db.session.commit()

        yield roles


@pytest.fixture
def token(client, user):
    with client.context:
        token = create_access_token(user.uuid)
        yield token
