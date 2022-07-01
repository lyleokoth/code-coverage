# -*- coding: utf-8 -*-
"""This module creates the flask extensions that we will use."""
import logging.config

from flasgger import LazyString, Swagger
from flask import request
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


def create_logger():
    """Create the application logger."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "json": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
            },
        },
        "handlers": {
            "standard": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "kinesis": {
                "class": "api.config.kinesis_config.KinesisFirehoseDeliveryStreamHandler",
                "formatter": "json"
            },
            "critical mail handler": {
                "class": "api.config.kinesis_config.CustomEmailLogger",
                "formatter": "json"
            }
        },
        "loggers": {
            "": {
                # "handlers": ["standard", "kinesis", "critical mail handler"],
                "handlers": ["standard"],
                "level": logging.INFO
            }
        }
    }

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    return logger


app_logger = create_logger()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Template API V4",
        "description": "Template for creating Flask APIs.",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "lyceokoth@gmail.com",
            "url": "www.twitter.com/lylethedesigner",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0"
    },
    "host": LazyString(lambda: request.host),
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example:\"Authorization: Bearer {token}\""
        }
    },
}


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(template=swagger_template,
                  config=swagger_config)
