import sqlalchemy
from app.models import Base, User
from flask.cli import with_appcontext
import click
import json

from app.util import create_user, delete_user_by_mail, update_users_password


def map_model_to_dict(model: Base):
    inspection = sqlalchemy.inspect(model)
    columns = [fields.key for fields in inspection.mapper.column_attrs]

    return {key: getattr(model, key) for key in columns}


def map_model_list_to_json(models):
    return list(map(map_model_to_dict, models))


def map_model_to_csv_row(model_dict, keys=[]):
    return ','.join([f'"{str(model_dict.get(key))}"' for key in keys])


def map_model_list_to_csv(model_dicts):
    cols = ['uuid', 'mail', 'is_confirmed', 'timestamp']
    def to_row(dict): return map_model_to_csv_row(dict, cols)
    header = ','.join([f'"{col}"' for col in cols])
    rows = list(map(to_row, model_dicts))

    return [header] + list(rows)


@click.command('add-user')
@click.argument('mail')
@click.argument('password')
@click.argument('alias', required=False)
@with_appcontext
def add_user(mail, password, alias):
    '''Add USER with PASSWORD and optional ALIAS.

    MAIL is the users mail or another unique identifer.

    PASSWORD the users password.

    ALIAS can be provided to be displayed instead of the users mail. If no value is provided, MAIL will be used as a fallback.
    '''
    try:
        user = create_user(mail, alias or mail, password)
        print(f'User {user.mail} with alias {user.alias} was added')
    except sqlalchemy.exc.IntegrityError:
        print(f'User {mail} already exists')


@click.command('delete-user')
@click.argument('mail')
@with_appcontext
def delete_user(mail):
    '''Delete user with MAIL.'''
    delete_user_by_mail(mail)
    print(f'User {mail} was deleted.')


@click.command('set-user-password')
@click.argument('mail')
@click.argument('password')
@with_appcontext
def set_user_password(mail, password):
    '''Set PASSWORD for USER'''
    try:
        update_users_password(mail, password)
        print(f'Password for user {mail} was updated.')
    except Exception:
        print('Error: Password was not set.')


@click.command('print-users')
@click.option('--csv', is_flag=True, default=False, help='print as csv')
@with_appcontext
def print_users(csv):
    '''Print a complete list of users with all informations.'''
    users = User.query.all()
    user_dicts = map_model_list_to_json(users)
    if csv:
        print(*map_model_list_to_csv(user_dicts), sep='\n')
    else:
        print(json.dumps(user_dicts))
