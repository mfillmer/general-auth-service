from app.models import User
from flask import Flask
from flask_jwt_extended import create_access_token


def test_token_is_verified(client: Flask):
    user = User(mail='user@test.com', password_hash='test')

    with client.context:
        client.db.session.add(user)
        client.db.session.commit()
        valid_token = create_access_token(
            identity=user.uuid, additional_claims=dict(verify_mail=True))
        token_without_claim = create_access_token(
            identity=user.uuid)
        token_without_valid_user = create_access_token(
            identity='test@test.com', additional_claims=dict(verify_mail=True))

        no_user = client.get(
            '/verify', query_string=dict(jwt=token_without_valid_user))
        no_token = client.get('/verify')
        not_allowed = client.get(
            '/verify', query_string=dict(jwt=token_without_claim))
        verify = client.get('/verify', query_string=dict(jwt=valid_token))

        assert no_user.status_code == 404
        assert b'not found' in no_user.data
        assert no_token.status_code == 401
        assert b'{"msg":"Missing \'jwt\' query paramater"}' in no_token.data
        assert b'not allowed' in not_allowed.data
        assert not_allowed.status_code == 403
        assert b'account verified' in verify.data
        assert verify.status_code == 200
        assert user.is_confirmed == True
