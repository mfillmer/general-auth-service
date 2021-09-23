def test_has_healthcheck(client):
    """sends status on root path"""

    answer = client.get('/')
    assert b'ok' in answer.data
