import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import decode_token
from app.models import User, db


def test_login(client):
    PW = 'test'
    user = User(mail='user@test.com',
                password_hash=generate_password_hash(PW))

    with client.context:
        db.session.add(user)
        db.session.commit()

    user_dict = json.dumps(dict(mail=user.mail, password=PW))

    non_json_request = client.post('/login', data=user_dict)
    assert non_json_request.status_code == 400

    correct_login = client.post('/login', data=user_dict,
                                content_type='application/json')
    assert correct_login.status_code == 200

    payload = json.loads(correct_login.data)
    access_token = payload.get('access_token')
    refresh_token = payload.get('refresh_token')
    access_token_payload = decode_token(access_token)
    refresh_token_payload = decode_token(refresh_token)

    assert access_token_payload.get('sub') == user.uuid
    assert refresh_token_payload.get('sub') == user.uuid

    login_not_existing_user = client.post(
        '/login', data=json.dumps(dict(mail='not_found', password='PW')),
        content_type='application/json')

    wrong_password = client.post(
        '/login', data=json.dumps(dict(mail=user.mail, password='PW*2')),
        content_type='application/json')

    assert login_not_existing_user.status_code == 404
    assert wrong_password.status_code == 401
