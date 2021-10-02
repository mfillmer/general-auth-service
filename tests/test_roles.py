from app.models import Role
from app.role import create_role, delete_roles, print_roles
import json


def test_create_roles(cli_runner, context, roles):
    with context:
        roles = Role.query.all()
        assert len(roles) == 1
        cli_runner.invoke(create_role, ['testing_role'])
        roles = Role.query.all()
        assert len(roles) == 2
        cli_runner.invoke(create_role, ['testing_role_1', 'testing_role_2'])
        roles = Role.query.all()
        assert len(roles) == 4
        cli_runner.invoke(create_role, ['testing_role_1', 'testing_role_2'])
        roles = Role.query.all()
        assert len(roles) == 4


def test_prints_permission_list_as_json(cli_runner, roles):
    result = cli_runner.invoke(print_roles)
    parsed_output = json.loads(result.output)

    assert type(parsed_output) is list
    assert len(parsed_output) == 1

    for role in roles:
        assert role.name in parsed_output


def test_prints_permission_list_as_csv(cli_runner, roles):
    result = cli_runner.invoke(print_roles, ['--csv'])
    role_list = [role.name for role in roles]
    assert result.exit_code == 0
    assert result.output == '\n'.join(role_list) + '\n'


def test_delete_roles(cli_runner, roles):
    roles_in_db = [perm.name for perm in Role.query.all()]
    assert len(roles_in_db) == 1
    result = cli_runner.invoke(delete_roles, roles_in_db)
    assert result.exit_code == 0
    roles_in_db = [perm.name for perm in Role.query.all()]
    assert len(roles_in_db) == 0


def test_set_roles_on_user():
    pass


def test_set_permissions_on_role():
    pass
