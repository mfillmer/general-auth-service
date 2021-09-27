from flask_jwt_extended.utils import create_access_token
from werkzeug.security import generate_password_hash
from app.models import User
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
    yield app.test_cli_runner()


@pytest.fixture
def client(app, context):

    with app.test_client() as client:
        with app.app_context() as context:
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
def token(client, user):
    with client.context:
        token = create_access_token(user.uuid)
        yield token
