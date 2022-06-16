# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
from flask import Blueprint
from flask_jwt_extended import jwt_required

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static', url_prefix='/api/auth')


@auth.route('/register', methods=['GET'])
def register():
    """Create a new Admin User."""
    return 'regstered!', 201


@auth.route('/login', methods=['GET'])
def login():
    """Log in a registered Admin."""
    return 'logged in', 200


@auth.route('/me', methods=['GET'])
@jwt_required()
def get_admin():
    """Get admin details."""
    return 'Admin', 200
