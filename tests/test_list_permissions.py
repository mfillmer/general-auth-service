import json
from flask.testing import FlaskCliRunner
from app.models import Permission

from app.permissions import print_permissions


def test_command_exists(cli_runner: FlaskCliRunner, permissions):
    result = cli_runner.invoke(print_permissions)

    assert result.exit_code == 0


def test_prints_permission_list_as_json(cli_runner: FlaskCliRunner, permissions: Permission):
    result = cli_runner.invoke(print_permissions)
    parsed_output = json.loads(result.output)

    assert type(parsed_output) is list
    assert len(parsed_output) == 5

    for perm in permissions:
        assert perm.name in parsed_output


def test_prints_permission_list_as_csv(cli_runner: FlaskCliRunner, permissions: Permission):
    result = cli_runner.invoke(print_permissions, ['--csv'])
    perm_list = [perm.name for perm in permissions]
    assert result.exit_code == 0
    assert result.output == '\n'.join(perm_list) + '\n'
