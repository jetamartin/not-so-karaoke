""" Forms for Not-So_Karoke App """

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, Optional, Email, EqualTo
from flask_wtf import FlaskForm

class SearchForm(FlaskForm):
  """ Video Search form. """
  artist = StringField("Artist", validators=[InputRequired(), Length(min=2, max=20)])
  song = StringField("Song", validators=[Optional(), Length(min=6, max=30)]  )

class SignupForm(FlaskForm):
  """ Signup form """
  username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)] )
  password = PasswordField('New Password', validators=[InputRequired(), Length(min=2, max=30),
                                          EqualTo('confirm', message='Passwords must match')])
  confirm = PasswordField('Repeat Password', validators=[InputRequired(), Length(min=2, max=30)])
  email = StringField('Email Address', validators=[InputRequired(), Email()])
 
class LoginForm(FlaskForm):
  """ Login form """
  username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)] )
  password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=30) ])
  # submit = SubmitField('Login')