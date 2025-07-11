#!/usr/bin/python3
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os


class User(db.Model, UserMixin):
    """ User model """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    score = db.relationship("Score", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.email == os.getenv('ADMIN_USER_EMAIL')
