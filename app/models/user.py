#!/usr/bin/python3
from app import db
""" User model """

class User(db.Model):
    """ User model """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    score = db.relationship("Score", backref="user", lazy=True) # one to many relationship