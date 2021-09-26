from app.models import User, db
from flask import Blueprint
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
