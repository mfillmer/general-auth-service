import json


def test_update_password_with_token_and_old_pw_succeeds(client, token, user):
    headers = dict(Authorization=f'Bearer {token}')
    headers['Content-Type'] = 'application/json'
    data = dict(
        old='test',
        new='test2'
    )
    answer = client.put('/account/password',
                        data=json.dumps(data), headers=headers)

    assert answer.status_code == 200
    data['mail'] = user.mail
    data['password'] = data['new']

    login_new = client.post('/login', data=json.dumps(dict(mail=user.mail, password=data['new'])),
                            content_type='application/json')
    login_old = client.post('/login', data=json.dumps(dict(mail=user.mail, password=data['old'])),
                            content_type='application/json')

    assert login_new.status_code == 200
    assert login_old.status_code == 401


def test_update_pw_fails_without_token(client):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(dict(
        old='test',
        new='test2'
    ))
    answer = client.put('/account/password', data=data, headers=headers)

    assert answer.status_code == 401


def test_update_pw_fails_wrong_password(client, token):
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}
    data = json.dumps(dict(
        old='test123',
        new='test2'
    ))
    answer = client.put('/account/password', data=data, headers=headers)

    assert answer.status_code == 403
