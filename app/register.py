import re
from app.models import User, db, Role, RoleOnUser
from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from uuid import uuid4
bp = Blueprint('register', __name__)


def is_mail_valid(mail: str) -> bool:
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(email_regex.match(mail))


@bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return 'json header not specified', 400

    data = request.json
    mail = data.get('mail')
    password = data.get('password')

    if not mail or not password:
        return 'bad request', 400

    if not is_mail_valid(mail):
        return 'mail is not valid', 400

    try:
        pw_hash = generate_password_hash(password)
        user_uuid = str(uuid4())
        user = User(uuid=user_uuid, mail=mail, password_hash=pw_hash)
        default_role = Role.query.filter_by(default=True).first()
        role_on_user = RoleOnUser(
            user_uuid=user_uuid, role_name=default_role.name)
        db.session.add(user)
        db.session.add(role_on_user)
        db.session.commit()

    except Exception as e:
        print(e)
        return 'user already exists', 422

    return 'ok', 200
