

from app.models import Permission
from app.permissions import delete_permissions


def test_permission_is_deleted_idempotently(cli_runner, permissions, context):
    perm_to_delete = permissions[1].name

    with context:
        perms_in_table = [perm.name for perm in Permission.query.all()]
        assert perm_to_delete in perms_in_table
        result = cli_runner.invoke(delete_permissions, [perm_to_delete])
        assert result.exit_code == 0
        perms_in_table = [perm.name for perm in Permission.query.all()]
        assert perm_to_delete not in perms_in_table
        result = cli_runner.invoke(delete_permissions, [perm_to_delete])
        assert result.exit_code == 0
        perms_in_table = [perm.name for perm in Permission.query.all()]
        assert perm_to_delete not in perms_in_table


def test_delete_multiple_permissions(cli_runner, permissions, context):
    perms_in_table = [perm.name for perm in Permission.query.all()]
    assert len(perms_in_table) == 5
    result = cli_runner.invoke(delete_permissions, perms_in_table)
    assert result.exit_code == 0
    perms_in_table = [perm.name for perm in Permission.query.all()]
    assert len(perms_in_table) == 0
