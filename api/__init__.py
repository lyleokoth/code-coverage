# -*- coding: utf-8 -*-
"""This module contains initialization code for the api package."""
import os
import sys

from dotenv import load_dotenv
from flasgger import LazyJSONEncoder, LazyString, Swagger
from flask import Flask
from flask_cors import CORS

from .blueprints.api.views import api
from .blueprints.auth.models import User
from .blueprints.auth.views import auth
from .blueprints.default.views import default
from .blueprints.extensions import app_logger, db, login_manager, ma, swagger
from .error_handlers import handle_bad_request
from .extensions import github_blueprint, jwt, migrate
from .helpers import are_environment_variables_set, set_flask_environment

load_dotenv()


if not are_environment_variables_set():
    msg = 'Unable to set Environment variables. Application existing...'
    app_logger.critical(msg)
    sys.exit(1)


app = Flask(__name__)
CORS(app)
app_logger.info('Successfully created the application instance.')
app.register_blueprint(default)
app_logger.info('Successfully registered the default blueprint.')
app.register_blueprint(auth)
app_logger.info('Successfully registered the auth blueprint.')
app.register_blueprint(api)
app_logger.info('Successfully registered the api blueprint.')
app.register_blueprint(github_blueprint, url_prefix="/login")
app_logger.info('Successfully registered the github blueprint.')

app.json_encoder = LazyJSONEncoder
swagger.init_app(app)

set_flask_environment(app)
app_logger.info('Successfully set the environment variables.')

app_logger.info(f"The configuration used is for {os.environ['FLASK_ENV']} environment.")
app_logger.info(f"The database connection string is {app.config['SQLALCHEMY_DATABASE_URI']}.")

db.init_app(app=app)
app_logger.info('Successfully initialized the database instance.')
migrate.init_app(app, db)
app_logger.info('Successfully initialized the migrate instance.')
jwt.init_app(app)
app_logger.info('Successfully initialized the JWT instance.')
login_manager.init_app(app)
app_logger.info('Successfully initialized the login manager instance.')
login_manager.login_view = 'github.login'
ma.init_app(app)
app_logger.info('Successfully initialized the Marshmallow instance.')


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Load the user with the given id."""
    return User.query.get(user_id)


app.register_error_handler(400, handle_bad_request)
app_logger.info('Successfully registered te 400 error handler.')
