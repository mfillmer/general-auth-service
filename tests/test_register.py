from flask import Flask
import json


def test_accepts_json_only(client: Flask):
    user = json.dumps(dict(
        mail='test@test.com',
        password='test'
    ))
    register = client.post('/register', data=user)
    assert b'json header not specified' in register.data
    assert register.status_code == 400


def test_register_new_user(client: Flask):
    user = json.dumps(dict(
        mail='test@test.com',
        password='test'
    ))
    register = client.post('/register', data=user,
                           content_type='application/json')
    assert b'ok' in register.data


def test_register_duplicate_user_returns_error(client):
    user = json.dumps(dict(
        mail='test@test.com',
        password='test'
    ))
    register = client.post('/register', data=user,
                           content_type='application/json')
    register = client.post('/register', data=user,
                           content_type='application/json')
    assert b'user already exists' in register.data
    assert register.status_code == 422


def test_register_checks_invalid_email(client):
    user = json.dumps(dict(
        mail='testtest.com',
        password='test'
    ))
    register = client.post('/register', data=user,
                           content_type='application/json')
    assert b'mail is not valid' in register.data
    assert register.status_code == 400
