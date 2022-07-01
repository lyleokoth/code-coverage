# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
from flask import Blueprint, jsonify, redirect, url_for
from flask_dance.contrib.github import github
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_login import login_required, logout_user

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static', url_prefix='/api/auth')


@auth.route("/login")
def login():  # pylint: disable=R1710
    """Log in a user."""
    if not github.authorized:
        return redirect(url_for('github.login'))
    res = github.get('/user')
    if res.ok:
        return redirect(url_for('default.dashboard'))


@auth.route('/profile', methods=['GET'])
# @jwt_required()
@login_required
def get_user_profile():
    """Get a logged in User's details."""
    return 'Admin', 200


@auth.route('/logout')
@login_required
def logout():
    """Log out a logged in user."""
    logout_user()
    return jsonify({'hello': 'You are logged out!'}), 200


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Create a refresh token."""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token), 201
