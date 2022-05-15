from . import db
from flask_login import UserMixin
from sqlalchemy import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock1 = db.Column(db.String(150))
    stock2 = db.Column(db.String(150))
    stock3 = db.Column(db.String(150))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))