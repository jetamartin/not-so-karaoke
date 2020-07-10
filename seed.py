""" Seed file to make sample data for db """

from models import db, User, Favorite
from app import app

#  Create all tables
db.drop_all()
db.create_all()

user1 = User(email="user1@mail.com", username = "user1")

db.session.add(user1)
db.session.commit()