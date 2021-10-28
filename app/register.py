from app.util import create_user
import re
from flask import Blueprint, request
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
    alias = data.get('alias', '')
    password = data.get('password')

    if not mail or not password:
        return 'bad request', 400

    if not is_mail_valid(mail):
        return 'mail is not valid', 400

    try:
        create_user(mail, alias, password)

    except Exception as e:
        print(e)
        return 'user already exists', 422

    return 'ok', 200
