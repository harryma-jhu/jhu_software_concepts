from flask import Flask 
def create_app():
    app = Flask(__name__)
    # .routes  = searching in folder vs global search 
    from .routes import bp 
    app.register_blueprint(bp)

    return app