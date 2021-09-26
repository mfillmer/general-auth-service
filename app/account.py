from app.models import User, db
from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity

bp = Blueprint('account', __name__)


@bp.route('/account', methods=['delete'])
@jwt_required()
def delete_account():
    uuid = get_jwt_identity()
    user = User.query.get(uuid)

    if user is None:
        return 'user does not exist', 404

    db.session.delete(user)
    db.session.commit()

    return 'account deleted', 202


@bp.route('/account/password', methods=['PUT'])
@jwt_required()
def update_password():
    if not request.is_json:
        return 'json format required', 400

    uuid = get_jwt_identity()
    user = User.query.get(uuid)
    data = request.json

    if user is None:
        return 'user does not exist', 404

    if not check_password_hash(user.password_hash, data.get('old')):
        return 'invalid credentials', 403

    user.password_hash = generate_password_hash(data['new'])
    db.session.commit()

    return 'ok', 200
