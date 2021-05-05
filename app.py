from flask import Flask
from API.Message.message_api import message_blueprint
from API.User.user_api import user_blueprint
from database import db, ma
from flasgger import APISpec, Swagger
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from models.message import MessageSchema
from models.user import UserSchema


def create_app():
    # ---------- App Configuration ----------
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configurations from Config class

    # Init SQLAlchemy and Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # Register Flask Blueprints
    app.register_blueprint(user_blueprint, url_prefix='/api/')
    app.register_blueprint(message_blueprint, url_prefix='/api/')

    # ---------- Swagger ----------
    # Create an APISpec
    spec = APISpec(
        title='CandidateFinder REST API',
        version='1.0',
        openapi_version='2.0',
        plugins=[FlaskPlugin(), MarshmallowPlugin()]
    )
    template = spec.to_flasgger(app, definitions=[UserSchema, MessageSchema])
    # Start Flasgger using a template from APISpec
    swag = Swagger(app, template=template)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
