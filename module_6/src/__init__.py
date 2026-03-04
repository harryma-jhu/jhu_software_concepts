from flask import Flask

def create_app():
    app = Flask(__name__)
    from .web.app.app import bp
    app.register_blueprint(bp)
    return app