#!/usr/bin/python3
from app import db
""" Subject model """


class Subject(db.Model):
    """ Subject model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quizzes = db.relationship('Quiz', backref='subject', lazy=True)
