from flask import Blueprint
from app.models import Request, db


bp = Blueprint('requests', __name__)


@bp.route('/')
def healthcheck():
    request = Request()
    db.session.add(request)
    db.session.commit()

    return 'ok', 200
