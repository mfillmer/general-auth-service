from app.util import init_db
import os

import pytest

from app import create_app, init_db


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            init_db
        yield client


def test_has_healthcheck(client):
    """sends status on root path"""

    answer = client.get('/')
    assert b'ok' in answer.data
