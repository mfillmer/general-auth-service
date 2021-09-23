from app.models import User, db
from flask import Blueprint, request
from werkzeug.security import generate_password_hash

bp = Blueprint('register', __name__)


@bp.route('/register', methods=['POST'])
def register():
    data = request.values
    mail = data.get('mail')
    password = data.get('password')

    if not mail or not password:
        return 'bad request', 400

    try:
        pw_hash = generate_password_hash(password)
        user = User(mail=mail, password_hash=pw_hash)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return 'user already exists', 422

    return 'ok', 200