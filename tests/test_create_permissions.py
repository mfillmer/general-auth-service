from app.models import Permission
from app.permissions import create_permission
from flask.testing import FlaskCliRunner


def test_command_exists(cli_runner: FlaskCliRunner, client):
    result = cli_runner.invoke(create_permission, ['TEST_PERM'])

    assert result.exit_code == 0
    assert result.output == 'permission created\n'
    result = cli_runner.invoke(create_permission, ['TEST_PERM1', 'TEST_PERM2'])

    assert result.output == '2 permissions created\n'


def test_permissions_get_persisted(cli_runner: FlaskCliRunner, context, client):
    items = ['TEST_PERM', 'TEST_PERM2']
    cli_runner.invoke(create_permission, items)

    with context:
        permissions = Permission.query.all()
        first = Permission.query.get(items[0])
        second = Permission.query.get(items[1])
    assert len(permissions) == 2
    assert first.name == items[0]
    assert second.name == items[1]
