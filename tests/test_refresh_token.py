from flask.testing import FlaskClient
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended.utils import decode_token
import json


def test_token_can_be_refreshed(client: FlaskClient, user):
    refresh_token = create_refresh_token(user.uuid)

    response = client.post(
        '/refresh', headers=dict(Authorization=f'Bearer {refresh_token}'))

    assert response.status_code == 200
    assert b'access_token' in response.data

    json_res = json.loads(response.data.decode())
    assert type(json_res) is dict
    token = json_res.get('access_token')
    payload = decode_token(token)

    assert payload['sub'] == user.uuid


def test_token_is_only_refreshed_when_authorized(client: FlaskClient):
    response = client.post(
        '/refresh')

    assert response.status_code == 401
