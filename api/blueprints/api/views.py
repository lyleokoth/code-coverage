# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
import json
import random

import pandas as pd
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static', url_prefix='/api')


@api.route('/data', methods=['POST'])
# @jwt_required()
def post_data():
    """Create new coverage data."""
    try:
        data = json.loads(request.json)
        test_df = pd.DataFrame(data)
    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400
    else:
        print(test_df)
        return data, 201


@api.route('/data', methods=['GET'])
# @jwt_required()
def get_data():
    """Create a new Admin User."""
    return 'regstered!', 200


@api.route('/badges', methods=['GET'])
# @jwt_required()
def get_badges():
    """Generate JSON data for the shields.io server.

    Parameters
    ----------
    username: str
        The users name

    Returns
    -------
    data: dict
        This dictionary contains info used to generate the dynamic badge by shields.io
            data = {
            "schemaVersion": 1,
            "label": "name",
            "message": "username",
            "color": "color-name",
            "labelColor": "color-name",
            "style": "style-name"
            }
    """
    if request.args.get('username'):
        username = request.args.get('username')
        colors = ['red', 'green', 'yellow', 'blue', 'orange', 'purple', 'grey']
        styles = ['flat', 'plastic', 'flat-square', 'for-the-badge', 'social']
        data = {
            "schemaVersion": 1,
            "label": "name",
            "message": username,
            "color": random.choice(colors),
            "labelColor": random.choice(colors),
            "style": random.choice(styles)
        }

        return data, 200

    error = {
        'error': 'You must include your name in the request.'
    }
    return error, 400
