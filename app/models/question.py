#!/usr/bin/python3
from app import db
""" Question model """


class Question(db.Model):
    """ Question model """
    id = db.Column(db.Integer, primary_key=True)
    statement = db.Column(db.Text)
    answer_1 = db.Column(db.String(200), nullable=False)
    answer_2 = db.Column(db.String(200), nullable=False)
    answer_3 = db.Column(db.String(200), nullable=False)
    answer_4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)