from flask import Blueprint, jsonify
from flask_jwt_extended.utils import get_jwt_identity
from app.models import User
from flask_jwt_extended import jwt_required
from app.util import get_user_access_token

bp = Blueprint('refresh', __name__)


@bp.route('/refresh', methods=['GET', 'POST'])
@jwt_required(refresh=True)
def refresh_user_token():
    uuid = get_jwt_identity()
    user = User.query.get(uuid)
    new_token = get_user_access_token(user)
    return jsonify(access_token=new_token)
