# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
from flask import Blueprint
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static', url_prefix='/api/')


@api.route('/data', methods=['POST'])
@jwt_required()
def post_data():
    """Create a new Admin User."""
    return 'regstered!', 201


@api.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    """Create a new Admin User."""
    return 'regstered!', 200


@api.route('/badges', methods=['GET'])
@jwt_required()
def get_badges():
    """Create a new Admin User."""
    return 'regstered!', 200
