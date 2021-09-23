from flask import Blueprint, jsonify
from app.models import Request, db


bp = Blueprint('requests', __name__)


@bp.route('/')
def healthcheck():
    request = Request()
    db.session.add(request)
    db.session.commit()

    return 'ok', 200


@bp.route('/print')
def report():
    items = Request.query.all()

    return jsonify(list(map(lambda item: item.to_dict(), items)))
