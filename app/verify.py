from app.models import User, db
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt, get_jwt_identity
bp = Blueprint('verify', __name__)


@bp.route('/verify', methods=['GET'])
@jwt_required(locations='query_string')
def verify_user_by_token():
    claims = get_jwt()
    uuid = get_jwt_identity()
    user = User.query.get(uuid)

    if not claims.get('verify_mail', False):
        return 'not allowed', 403

    if user is None:
        return 'not found', 404

    user.is_confirmed = True
    db.session.commit()

    return 'account verified', 200
