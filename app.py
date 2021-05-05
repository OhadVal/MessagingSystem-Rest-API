from flask import Flask

from API.Message.message_api import message_blueprint
from database import db, ma


def create_app():

    # ---------- App Configuration ----------
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configurations from Config class

    # Init SQLAlchemy and Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # Register Flask Blueprints
    app.register_blueprint(message_blueprint, url_prefix='/api/')

