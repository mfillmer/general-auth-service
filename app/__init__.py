from app.permissions import create_permissions, delete_permissions, print_permissions
from app.role import *
from app.users import add_user, delete_user, print_users, set_user_password
from flask import Flask
from app.models import db
from app.util import init_db
from app import register, verify, login, logout, account, refresh
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def setup_app(app: Flask):
    app.config.from_pyfile('./config.py')
    app.add_url_rule('/', view_func=lambda: ('ok', 200))
    # app.register_blueprint(register.bp)
    app.register_blueprint(verify.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(refresh.bp)


def init_modules(app: Flask):
    db.init_app(app)
    jwt = JWTManager(app)
    jwt.token_in_blocklist_loader(logout.check_if_token_is_revoked)

    if(app.debug):
        CORS(app)


def setup_cli(app: Flask):
    app.cli.add_command(init_db)
    app.cli.add_command(print_users)
    app.cli.add_command(add_user)
    app.cli.add_command(delete_user)
    app.cli.add_command(set_user_password)
    app.cli.add_command(create_permissions)
    app.cli.add_command(print_permissions)
    app.cli.add_command(delete_permissions)
    app.cli.add_command(create_role)
    app.cli.add_command(print_roles)
    app.cli.add_command(delete_roles)
    app.cli.add_command(set_permissions_on_role)
    app.cli.add_command(unset_permissions_on_role)
    app.cli.add_command(set_default_role)
    app.cli.add_command(unset_user_role)
    app.cli.add_command(set_user_role)


def create_app():
    app = Flask(__name__)

    setup_app(app)
    init_modules(app)
    setup_cli(app)

    return app
