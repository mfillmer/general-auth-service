from app.models import RevokedToken, db
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt


bp = Blueprint('logout', __name__)

invalidated_tokens = set()


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt().get('jti')
    rt = RevokedToken(jti=jti)
    db.session.add(rt)
    db.session.commit()
    return 'logged out', 202


def check_if_token_is_revoked(_, jwt_payload):
    jti = jwt_payload["jti"]
    return RevokedToken.query.get(jti) is not None
