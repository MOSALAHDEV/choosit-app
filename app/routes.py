#!/usr/bin/python3
from unicodedata import category
from app import create_app, db, login_manager
from flask import render_template, redirect, url_for, flash
from app.models import User, Subject, Quiz, Question, Score, question, quiz, user
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

app = create_app()


@app.cli.command('create-db')
def create_db():
    db.create_all()
    print("Database created successfully!")


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
                username=form.fullname.data,
                email=form.email.data,
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', category="success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid email or password', category="danger")
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash('User logged in successfully!', category="success")
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out successfully!', category="success")
    return redirect(url_for('login'))

@login_manager.user_loader
def loading_user(user_id):
    return User.query.get(user_id)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.is_admin:
                login_user(user)
                flash('Admin logged in successfully!', category="success")
                return redirect(url_for('admin_dashboard'))
            else:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('admin_login'))
        else:
            flash('Invalid email or password', category="danger")
    return render_template("/admin/login.html", form=form)


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('/admin/dashboard.html')

@app.route('/admin/manage_subject', methods=['GET', 'POST'])
@login_required
def admin_manage_subject():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    subject = Subject.query.all()
    return render_template('/admin/manage_subject.html', subject=subject)

@app.route('/admin/manage_quiz', methods=['GET', 'POST'])
@login_required
def admin_manage_quiz():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    quiz = Quiz.query.all()
    return render_template('/admin/manage_quiz.html', quiz=quiz)

@app.route('/admin/manage_question', methods=['GET', 'POST'])
@login_required
def admin_manage_question():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    question = Question.query.all()
    return render_template('/admin/manage_question.html', question=question)

@app.route('/admin/manage_user', methods=['GET', 'POST'])
@login_required
def admin_manage_user():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    user = User.query.all()
    return render_template('/admin/manage_user.html', user=user)

@app.route('/admin/manage_score', methods=['GET', 'POST'])
@login_required
def admin_manage_score():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    score = Score.query.all()
    return render_template('/admin/manage_score.html', score=score)