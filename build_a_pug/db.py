import sqlite3
import click
import os

from flask import current_app, g
from datetime import datetime


def get_db():
    """Uses Flask's special g object to create a database connection"""

    # Check if there is already a database connection associated with the Flask app
    # If not, create one and establish a cursor for it
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the database with the pug table"""

    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# Add CLI commands to initialize and delete the database
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("delete-db")
def delete_db_command():
    """Delete the SQLite database file."""

    database_file = current_app.config["DATABASE"]

    if database_file:
        os.remove(database_file)
        click.echo(f"Deleted the database file: {database_file}")
    else:
        click.echo("No database file found to delete.")


# Convert the `timestamp` datatype to a 12-hour datetime format, eg, 16:00 --> 4:00 PM
sqlite3.register_converter(
    "timestamp", lambda v: datetime.strptime(v.decode(), "%H:%M").strftime("%-I:%M %p")
)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(delete_db_command)


class DBError(Exception):
    """A database error."""

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv
