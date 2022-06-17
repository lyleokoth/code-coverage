# -*- coding: utf-8 -*-
"""This module contains the routes associated with the default Blueprint."""

from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from api.blueprints.auth.models import UserLoginSchema

default = Blueprint('default', __name__, template_folder='templates', static_folder='static')


@default.route('/', methods=['GET'])
@default.route('/index', methods=['GET'])
def home():
    """Confirm that the application is working."""
    if current_user:
        user_login_schema = UserLoginSchema()
        user_data = dict(
            message='hello from the sign up/in page',
            data=user_login_schema.dump(current_user)
        )
        return user_data, 200
    return jsonify({'hello': 'from the sign up/in page'}), 200


@default.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Get the dashboard."""
    user_login_schema = UserLoginSchema()
    user_data = dict(
        message='hello from the dashboard',
        data=user_login_schema.dump(current_user)
    )
    return user_data, 200
