from werkzeug.security import check_password_hash
from app.models import User
from app.util import get_user_access_token
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_refresh_token

bp = Blueprint('login', __name__)


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return 'json format required', 400

    payload = request.json
    mail = payload.get('mail')
    password = payload.get('password')

    user = User.query.filter_by(mail=mail).first_or_404()

    if not check_password_hash(user.password_hash, password):
        return 'invalid credentials', 401

    token = get_user_access_token(user)
    refresh_token = create_refresh_token(user.uuid)

    return jsonify(
        access_token=token,
        refresh_token=refresh_token
    ), 200
