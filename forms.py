
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class GuessWordForm(FlaskForm):
    """Form for guessing a word."""
    guess = StringField('Guess a word!', validators=[DataRequired()])