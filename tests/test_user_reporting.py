from app.users import print_users
from flask.testing import FlaskCliRunner
import json


def test_prints_list_of_users_as_json(cli_runner: FlaskCliRunner, user):
    result = cli_runner.invoke(print_users)

    parsed_output = json.loads(result.output)

    assert type(parsed_output) == list
    assert len(parsed_output) == 1
    assert parsed_output[0].get('mail') == user.mail
    assert parsed_output[0].get('uuid') == user.uuid
    assert parsed_output[0].get('timestamp') == user.timestamp


def test_prints_list_of_users_as_csv(cli_runner: FlaskCliRunner, user):
    result = cli_runner.invoke(print_users, ['--csv'])

    header = 'uuid;mail;is_confirmed;timestamp\n'
    row = f'{user.uuid};{user.mail};{user.is_confirmed};{user.timestamp}\n'

    assert result.output is not None
    assert result.output == header + row
