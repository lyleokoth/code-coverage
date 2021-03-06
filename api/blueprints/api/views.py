# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
import json
import random

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import desc

from ..auth.models import User, UserSchema
from .helpers import handle_post_data
from .models import Badge, BadgeSchema, Project, ProjectSchema, Run, RunSchema

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static', url_prefix='/api')


@api.route('/data', methods=['POST'])
@jwt_required()
def post_data():
    """Create new test data.

    This route is accessed at each run of our action.
    """
    try:
        test_data = json.loads(request.json)
        user_id = get_jwt_identity()
    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400
    else:
        return handle_post_data(user_id, test_data)


@api.route('/data/user', methods=['GET'])
# @jwt_required()
def get_user_data():
    """Get the test data for all the projects."""
    user = User.query.filter_by(id=1).first()
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200


@api.route('/data/project', methods=['GET'])
# @jwt_required()
def get_project_data():
    """Get the test data for a single project."""
    project_runs = Run.query.filter_by(project_id=1)
    runs_schema = RunSchema(many=True)
    return jsonify(runs_schema.dump(project_runs)), 200


@api.route('/data/run', methods=['GET'])
# @jwt_required()
def get_project_run_data():
    """Get the test data for a single project run."""
    project_run = Run.query.filter_by(id=1)
    run_schema = RunSchema(many=True)
    return jsonify(run_schema.dump(project_run)), 200


@api.route('/badges/authorize', methods=['GET'])
# @jwt_required()
def authorize_badges():
    """Authorize the creation of badges for your projects.

    This route is accessed one time for each project
    """
    badges = request.json['badges']
    project = Project.query.filter_by(id=1).first()
    if project:
        project.authorized = True
        project.badges = badges
        return jsonify({'success': 'authorized'}), 200
    return jsonify({'message': 'authorization failure'})


@api.route('/badge-markdown', methods=['GET'])
def get_badge_markdown():
    """Get the badge markdown.

    Supply the badge-name, project-name.
    """
    shields_io_endpoint = 'https://img.shields.io/endpoint'
    styling = 'style=plastic'
    url = 'https%3A%2F%2Foryks-code-coverage-dev.herokuapp.com%2Fapi%2Fbadge'
    username = 'lyleokoth'
    projectname = 'flask-social-auth'
    badgename = 'coverage-total'
    base = '![Custom badge]'
    badge_markdown = f"{base}({shields_io_endpoint}?{styling}&url={url}%2F{username}%2F{projectname}%2F{badgename})"
    return badge_markdown


@api.route('/badge/<username>/<projectname>/<badgename>', methods=['GET'])
def get_badge(username, projectname, badgename):  # pylint: disable=R0911
    """Generate JSON data for the shields.io server for a single badge.

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
    user = User.query.filter_by(username=username).first()
    if not user:
        data = {
            "schemaVersion": 1,
            "label": "error",
            "message": "invalid username",
            "color": "red",
            "labelColor": "green",
            "style": "for-the-badge"
        }
        return data, 200

    project = Project.query.filter_by(name=projectname).first()
    if not project:
        data = {
            "schemaVersion": 1,
            "label": "error",
            "message": "invalid projectname",
            "color": "red",
            "labelColor": "green",
            "style": "for-the-badge"
        }
        return data, 200

    run = Run.query.filter_by(project_id=project.id).first()
    if not run:
        data = {
            "schemaVersion": 1,
            "label": "error",
            "message": "missing test data",
            "color": "red",
            "labelColor": "green",
            "style": "for-the-badge"
        }
        return data, 200

    if badgename not in ['coverage-total']:
        data = {
            "schemaVersion": 1,
            "label": "error",
            "message": "Invalid badge name",
            "color": "red",
            "labelColor": "green",
            "style": "for-the-badge"
        }
        return data, 200

    run_id = Run.query.filter_by(project_id=1).order_by(desc(Run.id)).first().id

    badge = Badge.query.filter_by(run_id=run_id).first()

    return badge.get_badge(), 200
