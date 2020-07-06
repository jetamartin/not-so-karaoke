""" Forms for Not-So_Karoke App """

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Optional
from flask_wtf import FlaskForm

class SearchForm(FlaskForm):
  """ Video Search form. """
  artist = StringField(
    "Artist", 
    validators=[InputRequired(), Length(min=2, max=20)]
  )
  song = StringField(
    "Song", 
    validators=[Optional(), Length(min=6, max=30)]
  )