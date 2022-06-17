# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
import json

import pandas as pd
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import desc

from ..extensions import db
from .models import Badge, BadgeSchema, Project, Run

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static', url_prefix='/api')


@api.route('/data', methods=['POST'])
@jwt_required()
def post_data():
    """Create new test data.

    This route is accessed at each run of our action.
    """
    try:
        data = json.loads(request.json)
        # df_data = json.loads(data['data'])
        # test_df = pd.DataFrame(df_data)
        # print(data['user'])
    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400
    else:
        # print(test_df)
        user_id = get_jwt_identity()
        project = Project.query.filter_by(name=data['user']['project']).first()
        if project is None:
            cars = ["Ford", "Volvo", "BMW"]
            project = Project(name=data['user']['project'], user_id=user_id, project_badges=cars)
            db.session.add(project)
            db.session.commit()
            # print('Creatd project.')
            project = Project.query.filter_by(name=data['user']['project']).first()
            run = Run(project_id=project.id, results=data['data'])
            db.session.add(run)
            db.session.commit()
            # print('Created run')
            runs = Run.query.filter_by(project_id=1).order_by(desc(Run.id)).first()
            # print(runs)
            badge = Badge(run_id=runs.id)
            db.session.add(badge)
            db.session.commit()
            # print(badge)
            return data, 201
        run = Run(project_id=project.id, results=data['data'])
        db.session.add(run)
        db.session.commit()
        # print('Created run')
        # runs = Run.query.filter_by(project_id=1).order_by(desc(Run.id)).all()
        runs = Run.query.filter_by(project_id=1).order_by(desc(Run.id)).first()
        # print(runs)
        badge = Badge(run_id=runs.id)
        db.session.add(badge)
        db.session.commit()
        # print(badge)
        # project.project_badges.append('Toyota')
        # print(project)
        return jsonify({'request': 'successful!'}), 200


@api.route('/data/user', methods=['GET'])
# @jwt_required()
def get_user_data():
    """Get the test data for all the projects."""
    projects = Project.query.all()
    return jsonify(projects), 200


@api.route('/data/project', methods=['GET'])
# @jwt_required()
def get_project_data():
    """Get the test data for a single the projects."""
    project_runs = Run.query.filter_by(project_id=1)
    return jsonify(project_runs), 200


@api.route('/data/run', methods=['GET'])
# @jwt_required()
def get_project_run_data():
    """Get the test data for a single project run."""
    return 'All data for a single project run!', 200


@api.route('/badges/authorize', methods=['GET'])
# @jwt_required()
def authorize_badges():
    """Authorize the creation of badges for your projects.

    This route is accessed one time for each project
    """
    # badges = request.json['badges']
    # Then update authorize


@api.route('/badge', methods=['GET'])
def get_badge():
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
    # user_name = 'lyle'
    # project_name = 'flask-social-auth'
    run_id = None
    # badge_name = 'coverage'
    project_id = 1

    if not run_id:
        run_id = Run.query.filter_by(project_id=project_id).order_by(desc(Run.id)).first().id

    badge = Badge.query.filter_by(run_id=run_id).first()
    # print(badge)

    badge_schema = BadgeSchema()
    return badge_schema.dump(badge), 200
