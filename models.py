"""SQLAlchemy models for Not-So-Karaoke."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id= {u.id} username= {u.username} password= {u.password} email= {u.email}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    image_url = db.Column( db.Text, default="/static/images/default-pic.png")
    favorites = db.relationship('Favorite')

    @classmethod
    def signup(cls, username, password, email):
        """ Register user w/hashed password & return user. """

        hashed = bcrypt.generate_password_hash(password)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed password
        return cls(username=username, password=hashed_utf8, email=email)

    @classmethod
    def authenticate(cls, username, password):
        """ Validate that user exists and password is correct
        Return user if valid, else return false"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False



class Favorite(db.Model):
    """ Stores info about a users Favorite Video"""

    __tablename__ = 'favorites'

    def __repr__(self):
        f = self
        return f"<Favorite id= {f.id} user_id= {f.user_id} thumbnail = {f.thumbnail} video_id= {f.video_id} video_title= {f.video_title} artist_name= {f.artist_name} song_title= {f.song_title} notes= {f.notes}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    thumbnail = db.Column(
        db.String(50),
        nullable=False
    )

    video_id = db.Column(
        db.String(20),
        nullable=False
    )

    video_title = db.Column(
        db.String(100),
        nullable=False
    )

    artist_name = db.Column(
        db.String(100)
    )

    song_title = db.Column(
        db.String(100)
    )

    notes = db.Column(
        db.String(250)
    )

    user = db.relationship('User')
