from app.models import Permission, db
from flask.cli import with_appcontext
import click


@click.command('add-permission')
@click.argument('permission', required=True, nargs=-1)
@with_appcontext
def create_permission(permission):

    for item in permission:
        db.session.add(Permission(name=item))

    db.session.commit()

    if len(permission) == 1:
        print('permission created')
    else:
        print(f'{len(permission)} permissions created')
