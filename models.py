"""SQLAlchemy models for Not-So-Karaoke."""

from datetime import datetime

# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# bcrypt = Bcrypt()
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.String(40), nullable=False, unique=True )
    image_url = db.Column( db.Text, default="/static/images/default-pic.png")


class Favorite(db.Model):
    """ Stores info about a users Favorite Video"""

    __tablename__ = 'favorites'

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


    video_id = db.Column(
        db.String(20),
        nullable=False
    )

    video_title = db.Column(
        db.String(50)
    )

    artist_name = db.Column(
        db.String(50)
    )

    song_title = db.Column(
        db.String(50)
    )

    notes = db.Column(
        db.String(250)
    )


