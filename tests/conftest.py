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
