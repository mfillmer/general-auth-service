import json
import click
from flask.cli import with_appcontext

from app.models import PermissionOnRole, Role, db


@click.command('create-role')
@click.argument('roles', required=True, nargs=-1)
@with_appcontext
def create_role(roles):
    entries = [Role(name=role) for role in roles]

    db.session.add_all(entries)
    db.session.commit()


@click.command('print-roles')
@click.option('--csv', is_flag=True, default=False)
@with_appcontext
def print_roles(csv):
    roles = Role.query.all()
    list = [role.name for role in roles]

    if(csv):
        print(*list, sep='\n')
    else:
        print(json.dumps(list))


@click.command('delete-role')
@click.argument('roles', required=True, nargs=-1)
@with_appcontext
def delete_roles(roles):
    for role in roles:
        Role.query.filter_by(name=role).delete()

    db.session.commit()


@click.command('delete-role')
@click.argument('role', required=True)
@click.argument('permissions', required=True, nargs=-1)
@with_appcontext
def set_permissions_on_role(role, permissions):
    perms_on_role = [PermissionOnRole(
        role=role, perm=permission) for permission in permissions]
    db.session.add_all(perms_on_role)
    db.session.commit()
