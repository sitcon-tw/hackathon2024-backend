import os
from datetime import timedelta
from flask import Flask

def create_app(env):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

    from .views import bp
    app.register_blueprint(bp, url_prefix="/api")

    return app
