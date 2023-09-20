from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.fields import *

class ExampleForm(FlaskForm):
    """An example form that contains all the supported bootstrap style form fields."""
    name = StringField() # will not autocapitalize on mobile
    age = StringField() # will not autocapitalize on mobile
    home = StringField() # will not autocapitalize on mobile
    puppy_dinner = StringField(render_kw={'placeholder': 'e.g. 5:00 PM'}) # will not autocapitalize on mobile
    submit = SubmitField()

def create_app(configfile=None):
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    app.config['SECRET_KEY'] = 'any secret string'
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'
    app.config.from_pyfile('settings.py')

    @app.route("/")
    def index():
        form = ExampleForm()
        return render_template('index.html', form=form)
    
    return app

if __name__ == '__main__':
    create_app().run(debug=True)