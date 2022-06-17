# -*- coding: utf-8 -*-
"""This module contains initialization code for the api package."""
import os
import sys

from dotenv import load_dotenv
from flask import Flask

from .blueprints.api.views import api
from .blueprints.auth.models import User
from .blueprints.auth.views import auth
from .blueprints.default.views import default
from .blueprints.extensions import db, login_manager, ma
from .error_handlers import handle_bad_request
from .extensions import github_blueprint, jwt, migrate
from .helpers import are_environment_variables_set, set_flask_environment

load_dotenv()


if not are_environment_variables_set():
    print('Application existing...')
    sys.exit(1)


app = Flask(__name__)
app.register_blueprint(default)
app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(github_blueprint, url_prefix="/login")

set_flask_environment(app)

print(f"The configuration used is for {os.environ['FLASK_ENV']} environment.")
print(f"The database connection string is {app.config['SQLALCHEMY_DATABASE_URI']}.")

db.init_app(app=app)
login_manager.init_app(app)
login_manager.login_view = 'github.login'
migrate.init_app(app, db)
jwt.init_app(app)
ma.init_app(app)


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Load the user with the given id."""
    return User.query.get(user_id)


app.register_error_handler(400, handle_bad_request)
