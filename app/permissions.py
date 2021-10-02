from app.models import Permission, db
from flask.cli import with_appcontext
import click
import json


@click.command('add-permission')
@click.argument('permission', required=True, nargs=-1)
@with_appcontext
def create_permissions(permission):

    for item in permission:
        db.session.add(Permission(name=item))

    db.session.commit()

    if len(permission) == 1:
        print('permission created')
    else:
        print(f'{len(permission)} permissions created')


@click.command('print-permissions')
@click.option('--csv', is_flag=True, default=False)
@with_appcontext
def print_permissions(csv):
    permissions = Permission.query.all()
    list = [perm.name for perm in permissions]

    if(csv):
        print(*list, sep='\n')
    else:
        print(json.dumps(list))


@click.command('delete-permission')
@click.argument('permissions', required=True, nargs=-1)
@with_appcontext
def delete_permissions(permissions):
    for permission in permissions:
        Permission.query.filter_by(name=permission).delete()

    db.session.commit()
