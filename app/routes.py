#!/usr/bin/python3
from app import create_app, db
from flask import render_template
from app.models import User, Subject, Quiz, Question, Score


app = create_app()
@app.cli.command('create-db')
def create_db():
    db.create_all()
    print("Database created successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
