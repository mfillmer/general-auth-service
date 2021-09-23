from flask import Flask
from app.models import db
from app.request_logger import bp
from app.util import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('./config.py')

    db.init_app(app)

    app.register_blueprint(bp)

    app.cli.add_command(init_db)

    return app
