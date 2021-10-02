from flask_jwt_extended.utils import create_access_token
from werkzeug.security import generate_password_hash
from app.models import User, Permission, Role
import pytest
import os

from app import create_app, db


@pytest.fixture
def app():
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app = create_app()

    yield app


@pytest.fixture
def context(app):
    yield app.app_context()


@pytest.fixture
def cli_runner(app):
    with app.app_context():
        db.create_all()
        db.drop_all()
        cli_runner = app.test_cli_runner()
        cli_runner.db = db

        yield cli_runner


@pytest.fixture
def client(app, context):

    with app.test_client() as client:
        with context:
            db.create_all()
            client.db = db
            client.context = context
            yield client
            db.drop_all()


@pytest.fixture
def user(client):
    with client.context:
        db = client.db
        user = User(mail='user@test.com',
                    password_hash=generate_password_hash('test'))
        db.session.add(user)
        db.session.commit()
        yield user


@pytest.fixture
def permissions(client):
    with client.context:
        db = client.db
        def to_model(index): return Permission(name=f'test {index}')
        permissions = list(map(to_model, range(5)))
        db.session.add_all(permissions)
        db.session.commit()

        yield permissions


@pytest.fixture
def roles(client):
    with client.context:
        db = client.db
        def to_model(index): return Role(name=f'test {index}', is_default=True)
        roles = list(map(to_model, range(1)))
        db.session.add_all(roles)
        db.session.commit()

        yield roles


@ pytest.fixture
def token(client, user):
    with client.context:
        token = create_access_token(user.uuid)
        yield token
