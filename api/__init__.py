# -*- coding: utf-8 -*-
"""This module contains initialization code for the api package."""
import os
import sys

from dotenv import load_dotenv
from flask import Flask

from .blueprints.auth.views import auth
from .blueprints.default.views import default
from .blueprints.extensions import db
from .error_handlers import handle_bad_request
from .extensions import migrate
from .helpers import are_environment_variables_set, set_flask_environment

load_dotenv()


if not are_environment_variables_set():
    print('Application existing...')
    sys.exit(1)


app = Flask(__name__)
app.register_blueprint(default)
app.register_blueprint(auth)

set_flask_environment(app)

print(f"The configuration used is for {os.environ['FLASK_ENV']} environment.")
print(f"The database connection string is {app.config['SQLALCHEMY_DATABASE_URI']}.")

db.init_app(app=app)
migrate.init_app(app, db)

app.register_error_handler(400, handle_bad_request)
