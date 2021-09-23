from flask import Flask


def test_register_new_user(client: Flask):
    user = dict(
        mail='test@test.com',
        password='test'
    )
    register = client.post('/register', data=user)
    assert b'ok' in register.data


def test_register_duplicate_user_returns_error(client):
    user = dict(
        mail='test@test.com',
        password='test'
    )
    register = client.post('/register', data=user)
    register = client.post('/register', data=user)
    assert b'user already exists' in register.data
    assert register.status_code == 422


def test_register_checks_invalid_email(client):
    user = dict(
        mail='testtest.com',
        password='test'
    )
    register = client.post('/register', data=user)
    assert b'mail is not valid' in register.data
    assert register.status_code == 400
