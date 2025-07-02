#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import DateTimeField, DateTimeLocalField, StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8)
    ])
    confirm_pass = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8)
    ])
    submit = SubmitField('Login')

class subjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=80)])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Add Subject')

class quizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired(), Length(min=2, max=80)])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    date_of_quiz = DateTimeLocalField('Date of Quiz', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    submit = SubmitField('Add Quiz')

class questionForm(FlaskForm):
    statement = StringField('Statement', validators=[DataRequired()])
    answer_1 = StringField('First Choice', validators=[DataRequired()])
    answer_2 = StringField('Second Choice', validators=[DataRequired()])
    answer_3 = StringField('Third Choice', validators=[DataRequired()])
    answer_4 = StringField('Fourth Choice', validators=[DataRequired()])
    
    correct_option = SelectField(
        'Correct Choice',
        choices=[('A', 'First Choice'), ('B', 'Second Choice'), ('C', 'Third Choice'), ('D', 'Fourth Choice')],
        validators=[DataRequired()])
    
    submit = SubmitField('Add Question')