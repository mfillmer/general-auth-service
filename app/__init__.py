from flask import Flask
from app.models import db
from app.util import init_db
from app import register, verify, login, logout
from flask_jwt_extended import JWTManager


def setup_app(app: Flask):
    app.config.from_pyfile('./config.py')
    app.add_url_rule('/', view_func=lambda: ('ok', 200))
    app.register_blueprint(register.bp)
    app.register_blueprint(verify.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(logout.bp)


def init_modules(app: Flask):
    db.init_app(app)
    jwt = JWTManager(app)
    jwt.token_in_blocklist_loader(logout.check_if_token_is_revoked)


def setup_cli(app: Flask):
    app.cli.add_command(init_db)


def create_app():
    app = Flask(__name__)

    setup_app(app)
    init_modules(app)
    setup_cli(app)

    return app
