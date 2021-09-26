from app.models import RevokedToken, User, db
from werkzeug.security import generate_password_hash
import json


def test_logout_with_token_succeeds(client):
    user = User(mail='test@test.com',
                password_hash=generate_password_hash('test'))

    with client.context:
        db.session.add(user)
        db.session.commit()

    json_payload = json.dumps(dict(mail=user.mail, password='test'))

    login = client.post('/login', data=json_payload,
                        content_type='application/json')

    access_token = json.loads(login.data).get('access_token')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    logout = client.post('/logout', headers=headers)

    assert logout.status_code == 202
    assert b'logged out' in logout.data


def test_logout_fails_without_token(client):
    logout = client.post('/logout')

    assert logout.status_code == 401


def test_logout_invalidates_token(client):
    user = User(mail='test@test.com',
                password_hash=generate_password_hash('test'))

    with client.context:
        db.session.add(user)
        db.session.commit()

    json_payload = json.dumps(dict(mail=user.mail, password='test'))

    login = client.post('/login', data=json_payload,
                        content_type='application/json')

    access_token = json.loads(login.data).get('access_token')

    headers = {'Authorization': f'Bearer {access_token}'}

    client.post('/logout', headers=headers)
    logout = client.post('/logout', headers=headers)

    assert logout.status_code == 401
    assert json.loads(logout.data).get('msg') == 'Token has been revoked'


def test_revoked_tokens_are_persisted_in_db(client):
    user = User(mail='test@test.com',
                password_hash=generate_password_hash('test'))

    with client.context:
        db.session.add(user)
        db.session.commit()

    json_payload = json.dumps(dict(mail=user.mail, password='test'))

    login = client.post('/login', data=json_payload,
                        content_type='application/json')

    access_token = json.loads(login.data).get('access_token')

    headers = {'Authorization': f'Bearer {access_token}'}

    with client.context:
        assert len(RevokedToken.query.all()) == 0
        client.post('/logout', headers=headers)
        assert len(RevokedToken.query.all()) > 0
