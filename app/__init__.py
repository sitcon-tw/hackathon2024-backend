from flask import Flask, Blueprint


def create_app(env):
    app = Flask(__name__)

    from .views import bp
    app.register_blueprint(bp, url_prefix="/api")

    return app
