import json


def test_delete_account_with_token_succeeds(client, token):
    headers = dict(Authorization=f'Bearer {token}')
    answer = client.delete('/account', headers=headers)

    assert answer.status_code == 202
    assert answer.data == b'account deleted'


def test_delete_account_without_token_fails(client):
    answer = client.delete('/account')
    assert answer.status_code == 401


def test_login_fails_after_delete(client, token, user):
    headers = dict(Authorization=f'Bearer {token}')
    headers['Content-Type'] = 'application/json'
    data = json.dumps(dict(password='test', mail=user.mail))

    login = client.post('/login', data=data, headers=headers)
    assert login.status_code == 200

    client.delete('/account', headers=headers)
    login = client.post('/login', data=data, headers=headers)
    assert login.status_code == 404


def test_delete_twice_fails(client, token):
    headers = dict(Authorization=f'Bearer {token}')
    client.delete('/account', headers=headers)
    answer = client.delete('/account', headers=headers)

    assert answer.status_code == 404
