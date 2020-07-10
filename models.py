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

    def __repr__(self):
        u = self
        return f"<User id= {u.id} username= {u.username} email= {u.email}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.String(40), nullable=False, unique=True )
    image_url = db.Column( db.Text, default="/static/images/default-pic.png")

    favorites = db.relationship('Favorite')

class Favorite(db.Model):
    """ Stores info about a users Favorite Video"""

    __tablename__ = 'favorites'

    def __repr__(self):
        f = self
        return f"<Favorite id= {f.id} user_id= {f.user_id} video_id= {f.video_id} video_title= {f.video_title} artist_name= {f.artist_name} song_title= {f.song_title} notes= {f.notes}>"

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

    user = db.relationship('User')
