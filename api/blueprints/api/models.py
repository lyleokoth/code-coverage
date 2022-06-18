# -*- coding: utf-8 -*-
"""This module contains the database models used by the auth blueprint."""
from dataclasses import dataclass

from sqlalchemy.dialects.postgresql import ARRAY, JSON

from ..extensions import db, ma


@dataclass
class Project(db.Model):
    """A class that represents a project.

    Attributes
    ----------
    id: int
        The unique project identifier
    name: str
        The unique name identifying a project, consits of username and repo name
    user_id: int
        The id of the user who cretated the project

    """

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(250), unique=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_runs: int = db.relationship('Run', backref='ran', lazy=True)
    authorized: bool = db.Column(db.Boolean(), default=False, nullable=False)
    project_badges: int = db.Column(ARRAY(db.String(10)))


class ProjectSchema(ma.Schema):
    """Schema for the Project."""

    class Meta:
        """The fileds to expose."""

        fields = ('name', 'authorized', 'project_badges')


@dataclass
class Run(db.Model):
    """A class that represents a project run.

    Attributes
    ----------
    id: int
        The unique run identifier
    run_id: int
        The github run id
    project_id: int
        The id of the project that was ran
    run_time: date
        The time when the project was run
    results: str
        The run results

    """

    id: int = db.Column(db.Integer, primary_key=True)
    run_id: int = db.Column(db.Integer)
    results: str = db.Column(JSON)
    project_id: int = db.Column(db.Integer, db.ForeignKey('project.id'))
    run_badges: int = db.relationship('Badge', backref='badge', lazy=True)

    def create_badges(self):
        """Create all badges for this run."""
        pass  # pylint: disable=W0107

    def create_badge(self, badge):
        """Create a particular badge for this run."""
        pass  # pylint: disable=W0107


class RunSchema(ma.Schema):
    """Schema for the Project."""

    class Meta:
        """The fileds to expose."""

        fields = ('run_id', 'results', 'run_badges')


@dataclass
class Badge(db.Model):  # pylint: disable=R0902
    """A class that represents a badge.

    Attributes
    ----------
    id: int
        The unique badge identifier
    name: str
        The unique name identifying a badge
    run_id: int
        The id of the run that this badge was created for

    """

    id: int = db.Column(db.Integer, primary_key=True)
    run_id: int = db.Column(db.Integer, db.ForeignKey('run.id'))
    schemaVersion: int = db.Column(db.Integer, nullable=False, default=1)
    label: str = db.Column(db.String(50), nullable=False, default='name')
    message: str = db.Column(db.String(50), nullable=False, default='lyle')
    color: str = db.Column(db.String(50), nullable=False, default='red')
    labelColor: str = db.Column(db.String(50), nullable=False, default='green')
    style: str = db.Column(db.String(50), nullable=False, default='for-the-badge')

    def __init__(self, run_id, label='coverage-total', message='lyle') -> None:
        """Create a new badge."""
        self.run_id = run_id
        self.label = label
        self.message = message


class BadgeSchema(ma.Schema):
    """Schema for the Project."""

    class Meta:
        """The fileds to expose."""

        fields = ('schemaVersion', 'label', 'message', 'color', 'labelColor', 'style')
