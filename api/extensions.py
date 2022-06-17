# -*- coding: utf-8 -*-
"""This module creates the flask extensions that we will use."""
import os

from flask import redirect, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.github import github, make_github_blueprint
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_login import LoginManager, current_user, login_user
from flask_migrate import Migrate
from sqlalchemy.orm.exc import NoResultFound

from .blueprints.auth.models import OAuth, User, UserLoginSchema
from .blueprints.extensions import db
from .helpers import get_user_data

login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

github_blueprint = make_github_blueprint(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):  # pylint: disable=W0613
    """Automatically log in a user after authentication."""
    info = github.get('/user')
    if info.ok:
        account_info = info.json()
        username = account_info['login']

        query = User.query.filter_by(username=username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        user = User.query.filter_by(username=username).first()
        if user:
            if user.access_token:
                pass
            else:
                access_token = create_access_token(user.id)
                refresh_token = create_refresh_token(user.id)
                print(access_token)
                user.access_token = access_token
                user.refresh_token = refresh_token
        login_user(user=user)
        # user_data = get_user_data(info.json())
