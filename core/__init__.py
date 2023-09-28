from flask import Flask
from config import config
from dotenv import load_dotenv
from flask_caching import Cache

load_dotenv()


def create_app(config_name, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Registering Blueprints
    from core.auth_app import bp as a_bp

    app.register_blueprint(a_bp)

    return app