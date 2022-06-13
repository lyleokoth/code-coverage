# -*- coding: utf-8 -*-
"""This module executes the application."""

from flask.cli import FlaskGroup

from api import app, db
from api.blueprints.default.models import User

cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    """Create the database and all the tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """Add two users."""
    db.session.add(User(email='test@example.com'))
    db.session.add(User(email='test1@example.com'))
    db.session.commit()


if __name__ == '__main__':
    cli()
