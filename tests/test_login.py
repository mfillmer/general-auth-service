import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import decode_token
from app.models import PermissionOnRole, Role, User, db
from uuid import uuid4
from app.util import create_user


def test_login(client, permissions, user, db):

    user_dict = json.dumps(dict(mail=user.mail, password='test'))

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
    assert access_token_payload.get('permissions') == []
    assert refresh_token_payload.get('sub') == user.uuid

    login_not_existing_user = client.post(
        '/login', data=json.dumps(dict(mail='not_found', password='PW')),
        content_type='application/json')

    wrong_password = client.post(
        '/login', data=json.dumps(dict(mail=user.mail, password='PW*2')),
        content_type='application/json')

    assert login_not_existing_user.status_code == 404
    assert wrong_password.status_code == 401


def test_login_with_permissions(client, permissions, db, context):
    with context:
        default_role = Role(name='stuff', is_default=True)
        example_perms = [PermissionOnRole(
            role='stuff', perm=perm.name) for perm in permissions]
        db.session.add(default_role)
        db.session.add_all(example_perms)
        db.session.commit()
    user = create_user('test@test.com', 'test', 'test')

    user_dict = json.dumps(dict(mail=user.mail, password='test'))

    correct_login = client.post('/login', data=user_dict,
                                content_type='application/json')

    payload = json.loads(correct_login.data)
    access_token = payload.get('access_token')
    access_token_payload = decode_token(access_token)

    assert set(access_token_payload.get('permissions')) == set([
        f'test {i}' for i in range(5)])
