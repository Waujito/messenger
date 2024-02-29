import os
from flask import Flask
from . import default_config
from .db import db, init_db, init_db_command
from .errorHandlers import register_errorhandlers

import logging


def create_app(config: dict | str | None = None):
    app = Flask(__name__)

    # load default configuration
    app.config.from_object(default_config)

    # load environment configuration
    if 'APP_CONF' in os.environ:
        app.config.from_envvar('APP_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif isinstance(config, str):
            app.config.from_pyfile(config)

    app.config.from_prefixed_env()

    setup_app(app)

    return app


def setup_app(app: Flask):
    db.init_app(app)

    app.cli.add_command(init_db_command)

    logging.basicConfig()

    if app.debug:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)
        with app.app_context():
            init_db()

    from .auth import auth  # noqa
    app.register_blueprint(auth)

    from .api import api  # noqa
    app.register_blueprint(api)

    register_errorhandlers(app)
