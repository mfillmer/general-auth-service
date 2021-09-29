from app.models import Base, User
from sqlalchemy import inspect
from flask.cli import with_appcontext
import click
import json


def map_model_to_dict(model: Base):
    inspection = inspect(model)
    columns = [fields.key for fields in inspection.mapper.column_attrs]

    return {key: getattr(model, key) for key in columns}


def map_model_list_to_json(models):
    return list(map(map_model_to_dict, models))


def map_model_to_csv_row(model_dict, keys=[]):
    return ';'.join([str(model_dict.get(key)) for key in keys])


def map_model_list_to_csv(model_dicts):
    cols = ['uuid', 'mail', 'is_confirmed', 'timestamp']
    def to_row(dict): return map_model_to_csv_row(dict, cols)
    header = ';'.join(cols)
    rows = list(map(to_row, model_dicts))

    return [header] + list(rows)


@click.command('print-users')
@click.option('--csv', is_flag=True, default=False)
@with_appcontext
def print_users(csv):
    users = User.query.all()
    user_dicts = map_model_list_to_json(users)
    if csv:
        print(*map_model_list_to_csv(user_dicts), sep='\n')
    else:
        print(json.dumps(user_dicts))
