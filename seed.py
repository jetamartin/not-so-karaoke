""" Seed file to make sample data for db """

from models import db, User, Favorite
from app import app
from models import User
#  Create all tables
db.drop_all()
db.create_all()

user1 = User.register(username = "user1", password = "password1", email="user1@mail.com")

db.session.add(user1)
db.session.commit()