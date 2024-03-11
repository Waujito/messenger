import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask import current_app
import click
from pathlib import Path
from os.path import dirname


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
Model: type[Base] = db.Model  # type: ignore

from . import models  # noqa


def init_db():
    with current_app.app_context():
        db.create_all()
        try:
            with open(Path(dirname(__file__), 'rawSQL.sql'), 'r') as sql:
                db.session.execute(sa.text(sql.read()))
                db.session.commit()
        except:
            print("Unable to init indexes")


@click.command("init-db")
def init_db_command():
    init_db()
    print("The database initialized.")
