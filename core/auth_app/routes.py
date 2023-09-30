from flask import g
from core.auth_app import bp
from core.decorators import login_required


@bp.route('/test', methods=['GET'])
@login_required
def test():
    context = {
        "user_id": g.user_id,
        "email": g.user
    }
    return context, 200