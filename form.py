from flask_wtf import FlaskForm
from wtforms.fields import *

class PugForm(FlaskForm):
    """An example form that contains all the supported bootstrap style form fields."""
    name = StringField() # will not autocapitalize on mobile
    age = StringField(render_kw={'placeholder': 'e.g. 14'}) # will not autocapitalize on mobile
    home = StringField() # will not autocapitalize on mobile
    puppy_dinner = StringField(render_kw={'placeholder': 'e.g. 5:00 PM'}) # will not autocapitalize on mobile
    submit = SubmitField(render_kw={ 'id': 'form-button', 'onclick': 'showProgressBar()'})

class FormError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv