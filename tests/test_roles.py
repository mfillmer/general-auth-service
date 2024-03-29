from werkzeug.security import generate_password_hash
from app.models import Permission, PermissionOnRole, Role, User
from app.role import create_role, delete_roles, print_roles, set_default_role, set_permissions_on_role, set_user_role, unset_user_role
import json
from app.util import create_user


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


def test_set_default_role(cli_runner, roles, context, user, db):
    roles = [Role(name=f'test {index}') for index in range(1, 4)]
    new_default_role = roles[1].name

    with context:
        db.session.add_all(roles)
        db.session.commit()

        result = cli_runner.invoke(set_default_role, [new_default_role])

        assert result.exit_code == 0

        default = Role.query.get(new_default_role)
        all_defaults = Role.query.filter_by(is_default=True).all()

        assert default.is_default
        assert len(all_defaults) == 1

        new_user = create_user('tst@com.test', 'test', 'asdf')

        assert new_default_role in list(
            map(lambda role: role.name, new_user.roles))


def test_set_permissions_on_role(cli_runner, permissions, roles, context):
    all_perms = [perm.name for perm in permissions]
    role_name = roles[0].name
    result = cli_runner.invoke(set_permissions_on_role, [
                               role_name, *all_perms])

    assert result.exit_code == 0

    with context:
        role = Role.query.get(role_name)
        assert role.permissions is not None
        assert len(role.permissions) == len(permissions)
        role_perms = [perm.name for perm in role.permissions]

        for perm in all_perms:
            assert perm in role_perms


def test_set_role_on_user(cli_runner, user, context, db):
    role_name = 'temp_role'
    role = Role(name=role_name)
    permissions = [Permission(name=f'temp {i}') for i in range(5)]

    with context:
        db.session.add_all([role, *permissions])
        db.session.commit()
        db.session.add_all(
            [PermissionOnRole(role=role.name, perm=perm.name)
             for perm in permissions]
        )
        db.session.commit()

        assert role.permissions == permissions

        result = cli_runner.invoke(set_user_role, [user.mail, role.name])

        assert result.exit_code == 0
        user = User.query.first()
        assert role_name in list(map(lambda role: role.name, user.roles))


def test_unset_role_on_user(cli_runner, context, db, permissions):
    with context:
        default_role = Role(name='stuff', is_default=True)
        db.session.add(default_role)
        db.session.commit()

        user = create_user('test@test.test123', 'test', 'test')
        user_uuid = user.uuid
        assert len(user.roles) == 1

        cli_runner.invoke(unset_user_role, [user.mail, default_role.name])

        user = User.query.get(user_uuid)

        assert len(user.permissions) == 0
