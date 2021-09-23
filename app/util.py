import click
from flask.cli import with_appcontext
from app.models import db


@click.command('init-db')
@with_appcontext
def init_db():

    print('drop all tables')
    db.drop_all()

    print('create all tables')
    db.create_all()
