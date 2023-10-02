from flask import Blueprint

bp = Blueprint('auth_app', __name__)


from core.auth_app import routes  # noqa: F401,E402
