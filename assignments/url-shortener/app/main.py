from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.shortener import shorten_bp
    app.register_blueprint(shorten_bp)

    return app

app = create_app()
