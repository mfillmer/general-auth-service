import json
import click
from flask.cli import with_appcontext
from app.models import PermissionOnRole, Role, User, db, RoleOnUser


@click.command('add-roles')
@click.argument('roles', required=True, nargs=-1)
@with_appcontext
def create_role(roles):
    '''create ROLES

    ROLES may take multiple terms, separated by spaces. Each term will create one role.
    '''
    entries = [Role(name=role) for role in roles]

    db.session.add_all(entries)
    db.session.commit()

    if len(roles) == 1:
        print('role created')
    else:
        print(f'{len(roles)} roles created')


@click.command('print-roles')
@click.option('--csv', is_flag=True, default=False, help='print as csv')
@click.option('--permissions', is_flag=True, default=False, help='show permissions')
@with_appcontext
def print_roles(csv, permissions):
    '''Print a complete list of existing roles.'''
    roles = Role.query.all()

    if permissions:
        list = [
            f'{role.name} -> [{", ".join([p.name for p in role.permissions])}]' for role in roles]
    else:
        list = [role.name for role in roles]

    if(csv):
        print(*list, sep='\n')
    else:
        print(json.dumps(list))


@click.command('delete-role')
@click.argument('roles', required=True, nargs=-1)
@with_appcontext
def delete_roles(roles):
    '''delete ROLES

    ROLES may take multiple terms, separated by spaces. Each term will delete the corresponding role.'''

    for role in roles:
        Role.query.filter_by(name=role).delete()

    db.session.commit()


@click.command('set-permissions-on-role')
@click.argument('role', required=True)
@click.argument('permissions', required=True, nargs=-1)
@with_appcontext
def set_permissions_on_role(role, permissions):
    '''Assign the specified ROLE a list of PERMISSIONS.'''
    perms_on_role = [PermissionOnRole(
        role=role, perm=permission) for permission in permissions]
    db.session.add_all(perms_on_role)
    db.session.commit()
    print(f'assigned {len(permissions)} permissions to {role}.')


@click.command('unset-permissions-on-role')
@click.argument('role', required=True)
@click.argument('permissions', required=True, nargs=-1)
@with_appcontext
def unset_permissions_on_role(role, permissions):
    '''REMOVE PERMISSIONS FROM ROLE.'''

    items = PermissionOnRole.query.filter(
        PermissionOnRole.role == role).all()

    for item in items:
        if item.perm in permissions:
            db.session.delete(item)

    db.session.commit()
    print(f'removed {len(permissions)} permissions from {role}.')


@click.command('set-default-role')
@click.argument('role', required=True)
@with_appcontext
def set_default_role(role):
    '''Set ROLE as default.

    New Users will be assigned the default role.'''
    role = Role.query.get(role)

    if role is not None:
        Role.query.update(values=dict(is_default=False))

        role.is_default = True
        db.session.commit()


@click.command('set-user-role')
@click.argument('user', required=True)
@click.argument('role', required=True)
@with_appcontext
def set_user_role(user, role):
    '''Assign USER a specified ROLE.'''
    user = User.query.filter_by(mail=user).first()

    try:
        connection = RoleOnUser(user_uuid=user.uuid, role_name=role)
        db.session.add(connection)
        db.session.commit()
    except:
        pass

    db.session.commit()


@click.command('unset-user-role')
@click.argument('user', required=True)
@click.argument('role', required=True)
@with_appcontext
def unset_user_role(user, role):
    '''Remove ROLE from USER.'''
    user = User.query.filter_by(mail=user).first()

    RoleOnUser.query.filter_by(user_uuid=user.uuid, role_name=role).delete()

    db.session.commit()
