# -*- coding: utf-8 -*-
"""This module contains initialization code for the api package."""
import os
import sys

from dotenv import load_dotenv
from flask import Flask

from .blueprints.default.views import default
from .blueprints.extensions import app_logger, db
from .error_handlers import handle_bad_request
from .extensions import migrate
from .helpers import are_environment_variables_set, set_flask_environment

load_dotenv()


if not are_environment_variables_set():
    msg = 'Unable to set Environment variables. Application existing...'
    app_logger.critical(msg)
    sys.exit(1)


app = Flask(__name__)
app_logger.info('Successfully created the application instance.')
app.register_blueprint(default)
app_logger.info('Successfully registered the default route.')


set_flask_environment(app)
app_logger.info('Successfully set the environment variables.')

app_logger.info(f"The configuration used is for {os.environ['FLASK_ENV']} environment.")
app_logger.info(f"The database connection string is {app.config['SQLALCHEMY_DATABASE_URI']}.")

db.init_app(app=app)
app_logger.info('Successfully initialized the database instance.')
migrate.init_app(app, db)
app_logger.info('Successfully initialized the migrate instance.')

app.register_error_handler(400, handle_bad_request)
app_logger.info('Successfully registered te 400 error handler.')
