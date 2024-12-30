from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from sqlite3 import IntegrityError
from wtforms.fields import *

import requests
import json
import os

from .pug import Pug, get_pug_facts, PugDB
from .form import PugForm, FormError
from .db import DBError, get_db, init_app

# Get the absolute path to the `instance` directory in `testing-strategies`
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
instance_path = os.path.join(project_root, "instance")


def create_app(configfile=None):
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
    bootstrap = Bootstrap5(app)
    app.config["SECRET_KEY"] = "any secret string"
    app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "minty"
    app.config["DATABASE"] = os.path.join(app.instance_path, "build_a_pug.sqlite")

    # Create the database connection
    # First ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Then initialize the database if it doesn't exist

    init_app(app)

    @app.errorhandler(FormError)
    def invalid_api_usage(e):
        error_message = e.to_dict()
        return render_template("formerror.html", error_message=error_message)

    @app.errorhandler(DBError)
    def db_error(e):
        error_message = e.to_dict()
        return render_template("dberror.html", error_message=error_message)

    @app.route("/", methods=["GET", "POST"])
    def index():
        form = PugForm()

        try:
            if request.method == "POST" and form.validate():
                pug = Pug(
                    form.name.data,
                    form.age.data,
                    form.home.data,
                    form.puppy_dinner.data,
                )
                pug_description = pug.describe_pug()
                pug_image = pug.build_pug()
                session["pug_description"] = pug_description
                session["pug_image"] = pug_image
                session["puppy_dinner"] = pug.puppy_dinner

                pug.description = pug_description
                pug.image = pug_image

                with app.app_context():
                    db = get_db()
                    PugDB.create_pug(db, pug)

                return redirect(url_for("heres_your_pug"))

        except ValueError as err:
            raise FormError(err.args[0])

        except IntegrityError:
            raise DBError(form.name.data)

        return render_template("index.html", form=form)

    @app.route("/heresyourpug", methods=["GET", "POST"])
    def heres_your_pug():
        return render_template(
            "heresyourpug.html",
            pug_description=session["pug_description"],
            pug_image=session["pug_image"],
        )

    @app.route("/seegrumble", methods=["GET", "POST"])
    def see_grumble():

        with app.app_context():
            db = get_db()
            grumble = PugDB.get_grumble(db)

        return render_template(
            "seegrumble.html",
            grumble=grumble,
        )

    @app.route("/puppydinner", methods=["GET", "POST"])
    def puppy_dinner():
        puppy_dinner_result = Pug.check_for_puppy_dinner(
            puppy_dinner=session["puppy_dinner"]
        )
        session["puppy_dinner_result"] = puppy_dinner_result
        return render_template(
            "heresyourpug.html",
            pug_description=session["pug_description"],
            pug_image=session["pug_image"],
            puppy_dinner_result=session["puppy_dinner_result"],
        )

    @app.route("/pugfacts", methods=["GET"])
    def pug_facts():
        pug_breed_facts = get_pug_facts()
        return render_template("pugfacts.html", pug_breed_facts=pug_breed_facts)

    return app
