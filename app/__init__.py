from flask import Flask
from app.models import db
from app.request_logger import bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('./config.py')

    db.init_app(app)

    app.register_blueprint(bp)

    return app
