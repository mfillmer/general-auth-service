from app.models import Base, User
from sqlalchemy import inspect
import click
import json


def map_model_to_dict(model: Base):
    inspection = inspect(model)
    columns = [fields.key for fields in inspection.mapper.column_attrs]

    return {key: getattr(model, key) for key in columns}


def map_model_list(models):
    return list(map(map_model_to_dict, models))


@click.command('print-users')
def print_users():
    users = User.query.all()
    user_dicts = map_model_list(users)
    print(json.dumps(user_dicts))
