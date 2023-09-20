from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.fields import *
from .pug import Pug

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

    @app.route("/", methods=['GET', 'POST'])
    def index():
        form = ExampleForm()
        if request.method == 'POST' and form.validate():
            pug = Pug(form.name.data, form.age.data, form.home.data, form.puppy_dinner.data)
            pug_description = pug.describe_pug()
            pug_image = pug.build_pug()
            session['pug_description'] = pug_description
            session['pug_image'] = pug_image
            session['puppy_dinner'] = pug.puppy_dinner

            return redirect(url_for('heres_your_pug'))
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