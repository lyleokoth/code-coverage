# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import json

import pandas as pd
from flask import jsonify
from sqlalchemy import desc

from ..extensions import db
from .models import Badge, Project, Run


def create_project(user_id: int, project_name: str):
    """Create a new project."""
    authorized = False
    project_badges = ['coverage-total']
    project = Project(name=project_name, user_id=user_id, authorized=authorized, project_badges=project_badges)
    db.session.add(project)
    db.session.commit()


def get_project_by_name(project_name: str):
    """Get a project with the given name."""
    project = Project.query.filter_by(name=project_name).first()
    return project


def create_run(project_id: int, run_id: int, passed: bool, results: dict):
    """Create a single run."""
    run = Run(project_id=project_id, results=results, run_id=run_id, passed=passed)
    db.session.add(run)
    db.session.commit()


def get_run_by_project(project_id: int):
    """Get a particular run."""
    run = Run.query.filter_by(project_id=project_id).order_by(desc(Run.id)).first()
    return run


def create_badge_data(passed: bool, project_id: int, run_id: int, results: dict):
    """Create the data needed to create a badge."""
    if passed:
        results = get_run_by_project(project_id).results
        df = pd.DataFrame(results)
        last_row = df.iloc[-1].tolist()
        coverage_total = last_row[-1]
        label = 'Coverage-Total'
        create_badge(run_id, label, coverage_total, passed)  # pylint: disable=E1121
    else:
        label = 'Tests'
        message = 'Failing'
        create_badge(run_id, label, message, passed)  # pylint: disable=E1121


def create_badge(run_id: int, label: str, message: str, passed: bool):
    """Create a badge for a single run."""
    badge = Badge(run_id=run_id, label=label, message=message, passed=passed)
    db.session.add(badge)
    db.session.commit()


def handle_post_data(user_id: int, test_data: dict):
    """Handle test data from a test run.

    Each time the action is run, this function handles the data from the test
    run.

    Attributes
    ----------
    user_id: int
        The user's id
    test_data: dict
        The test result
    """
    results = json.loads(test_data['data'])
    project_name = test_data['user']['project']
    # username = test_data['user']['username']
    passed = test_data['passed']
    run_id = test_data['run_number']
    project = Project.query.filter_by(name=project_name).first()

    if project is None:
        create_project(user_id, project_name)
        project_id = get_project_by_name(project_name).id
        create_run(project_id, run_id, passed, results)
        run_id = get_run_by_project(project_id).id
        create_badge_data(passed, project_id, run_id, results)
        return jsonify({'request': 'Project creation successful!'}), 201

    project_id = get_project_by_name(project_name).id
    create_run(project_id, run_id, passed, results)
    run_id = get_run_by_project(project_id).id
    create_badge_data(passed, project_id, run_id, results)
    return jsonify({'request': 'Project update successful!'}), 200
