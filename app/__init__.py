import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS

def create_app(env):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

    from .views import bp
    app.register_blueprint(bp, url_prefix="/api")
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    return app
