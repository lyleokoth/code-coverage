# -*- coding: utf-8 -*-
"""This module contains the routes associated with the default Blueprint."""
from json import JSONDecodeError

from flask import Blueprint, jsonify, redirect, request, url_for

from .helpers import handle_create_user, handle_delete_user, handle_get_user, handle_update_user
from .models import User

default = Blueprint('default', __name__, template_folder='templates', static_folder='static')


@default.route('/', methods=['GET'])
def default_route():
    """Confirm that the application is working."""
    return redirect(url_for('auth.register')), 302


@default.route('/home', methods=['GET'])
@default.route('/index', methods=['GET'])
def home():
    """Confirm that the application is working."""
    return jsonify({'hello': 'from template api'}), 200


@default.route('/user', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        data = request.json
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    else:
        return handle_create_user(data)


@default.route('/user', methods=['GET'])
def get_user():
    """Get a user with the given id."""
    try:
        user_id = int(request.args.get('id'))
    except ValueError as e:
        print(e)
        print('This error is cause by not supplying the user id')
        return 'The user id was not provided or the id is invalid.', 400
    else:
        return handle_get_user(user_id)


@default.route('/user', methods=['PUT'])
def update_user():
    """Update user details."""
    try:
        data = request.json
        user_id = int(request.args.get('id'))
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        print('This error is cause by not supplying the user id')
        return 'The user id was not provided', 400
    else:
        return handle_update_user(user_id, data)


@default.route('/user', methods=['DELETE'])
def delete_user():
    """Delete a user."""
    try:
        user_id = int(request.args.get('id'))
    except ValueError as e:
        print(e)
        print('This error is cause by not supplying the user id')
        return 'The user id was not provided', 400
    else:
        return handle_delete_user(user_id)


@default.route('/users', methods=['GET'])
def all_users():
    """Get all the users."""
    users = User.query.all()
    return jsonify(users), 200
