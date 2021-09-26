from flask_jwt_extended.utils import create_access_token
from werkzeug.security import generate_password_hash
from app.models import User
import pytest
import os

from app import create_app, db


@pytest.fixture
def client():
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app = create_app()

    with app.test_client() as client:
        with app.app_context() as context:
            db.create_all()
            client.context = context
            client.db = db
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
