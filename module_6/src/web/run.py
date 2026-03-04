"""Entry point for the Flask application."""
from flask import Flask
from app.app import bp 

def create_app():
    """Application factory to initialize the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    app = create_app()
    # Host 0.0.0.0 is required for Docker access
    app.run(host="0.0.0.0", port=8080, debug=False)