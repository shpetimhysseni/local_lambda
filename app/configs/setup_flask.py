from flask import Flask
from flask_cors import CORS

def setup_flask_app(config_file="app.configs.config.Config"):
    """Register and configure application and it's dependencies"""
    app = Flask(__name__)
    app.config.from_object(config_file)
    CORS(app)

    with app.app_context():
        from app.routes.routes import api
        app.register_blueprint(api)

    return app