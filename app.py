import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.fields import *
from .pug import Pug
from .form import PugForm, FormError

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

class Pug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    home = db.Column(db.String(100), unique=True, nullable=False)
    puppy_dinner = db.Column(b.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    image = db.Column(db.Text)

    def __repr__(self):
        return f'<Pug {self.name}>'

def create_app(configfile=None):
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'any secret string'
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'
    app.config.from_pyfile('settings.py')
    db = SQLAlchemy(app)
    

    @app.errorhandler(FormError)
    def invalid_api_usage(e):
        error_message = e.to_dict()
        return render_template("formerror.html", error_message=error_message)

    @app.route("/", methods=['GET', 'POST'])
    def index():
        form = PugForm()
        try:
            if request.method == 'POST' and form.validate():
                pug = Pug(form.name.data, form.age.data, form.home.data, form.puppy_dinner.data)
                pug_description = pug.describe_pug()
                pug_image = pug.build_pug()
                session['pug_description'] = pug_description
                session['pug_image'] = pug_image
                session['puppy_dinner'] = pug.puppy_dinner
                
                return redirect(url_for('heres_your_pug'))  
        except ValueError as err:
            raise FormError(err.args[0])
        
        return render_template('index.html', form=form)
    
    @app.route("/heresyourpug", methods=['GET', 'POST'])
    def heres_your_pug():
        return render_template('heresyourpug.html', pug_description=session['pug_description'], pug_image=session['pug_image'])

    @app.route("/puppydinner", methods=['GET', 'POST'])
    def puppy_dinner():
        puppy_dinner_result = Pug.check_for_puppy_dinner(puppy_dinner=session['puppy_dinner'])
        session['puppy_dinner_result'] = puppy_dinner_result
        return render_template('heresyourpug.html', pug_description=session['pug_description'], pug_image=session['pug_image'], puppy_dinner_result=session['puppy_dinner_result'])
    
    return app

if __name__ == '__main__':
    create_app().run(debug=True)