#!/usr/bin/python3
from app import create_app, db, login_manager
from flask import render_template, redirect, url_for, flash, request
from app.models import User, Subject, Quiz, Question, Score
from app.forms import RegisterForm, LoginForm, subjectForm, quizForm, questionForm
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
    """Register route"""
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
    """Login route"""
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
    """Dashboard route"""
    quizzes = Quiz.query.all()
    return render_template('dashboard.html', quizzes=quizzes)


@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('User logged out successfully!', category="success")
    return redirect(url_for('login'))


@login_manager.user_loader
def loading_user(user_id):
    return User.query.get(user_id)


# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login Route"""
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
    """admin dashboard route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('/admin/dashboard.html')


@app.route('/admin/manage_user', methods=['GET', 'POST'])
@login_required
def admin_manage_user():
    """admin manage user route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    user = User.query.all()
    return render_template('/admin/manage_user.html', user=user)


@app.route('/admin/manage_score', methods=['GET', 'POST'])
@login_required
def admin_manage_score():
    """admin manage score route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    score = Score.query.all()
    return render_template('/admin/manage_score.html', score=score)


# Subject Management Routes
@app.route('/admin/manage_subject', methods=['GET', 'POST'])
@login_required
def admin_manage_subject():
    """admin manage subject route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    subject = Subject.query.all()
    return render_template('/admin/manage_subject.html', subject=subject)


@app.route('/admin/add_subject', methods=['GET', 'POST'])
@login_required
def admin_add_subject():
    """admin add subject route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    form = subjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash('Subject saved successfully!', 'success')
        return redirect(url_for('admin_manage_subject'))
    return render_template('/admin/add_subject.html', form=form)


@app.route('/admin/edit_subject/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_subject(id):
    """admin edit subject route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    subject = Subject.query.get_or_404(id)
    form = subjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin_manage_subject'))
    return render_template('/admin/edit_subject.html', form=form)


@app.route('/admin/delete_subject/<int:id>', methods=['POST'])
@login_required
def admin_delete_subject(id):
    """admin delete subject route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    subject = Subject.query.get_or_404(id)
    if subject.quizzes:
        flash('Subject has quizzes, cannot be deleted.', 'danger')
        return redirect(url_for('admin_manage_subject'))
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin_manage_subject'))


# Quiz Management Routes
@app.route('/admin/manage_quiz', methods=['GET', 'POST'])
@login_required
def admin_manage_quiz():
    """admin manage quiz route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    quiz = Quiz.query.all()
    return render_template('/admin/manage_quiz.html', quiz=quiz)


@app.route('/admin/add_quiz', methods=['GET', 'POST'])
@login_required
def admin_add_quiz():
    """admin add quiz route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    form = quizForm()
    form.subject_id.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
    if form.validate_on_submit():
        quiz = Quiz(name=form.name.data, subject_id=form.subject_id.data, date_of_quiz=form.date_of_quiz.data, duration=form.duration.data)
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz saved successfully!', 'success')
        return redirect(url_for('admin_manage_quiz'))
    return render_template('/admin/add_quiz.html', form=form)


@app.route('/admin/edit_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_quiz(id):
    """admin edit quiz route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    quiz = Quiz.query.get_or_404(id)
    form = quizForm(obj=quiz)
    form.subject_id.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
    if form.validate_on_submit():
        quiz.name = form.name.data
        quiz.subject_id = form.subject_id.data
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.duration = form.duration.data
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin_manage_quiz'))
    return render_template('/admin/edit_quiz.html', form=form)


@app.route('/admin/delete_quiz/<int:id>', methods=['POST'])
@login_required
def admin_delete_quiz(id):
    """admin delete quiz route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    quiz = Quiz.query.get_or_404(id)
    Score.query.filter_by(quiz_id=id).delete(synchronize_session=False)
    for question in quiz.questions:
        db.session.delete(question)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin_manage_quiz'))


# Question Management Routes
@app.route('/admin/manage_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def admin_manage_question(quiz_id):
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('/admin/manage_question.html', questions=questions, quiz=quiz)

@app.route('/admin/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def admin_add_question(quiz_id):
    """admin add question route"""
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    quiz = Quiz.query.get_or_404(quiz_id)
    form = questionForm()
    if form.validate_on_submit():
        question = Question(
            statement=form.statement.data,
            answer_1=form.answer_1.data,
            answer_2=form.answer_2.data,
            answer_3=form.answer_3.data,
            answer_4=form.answer_4.data,
            correct_option=form.correct_option.data,
            quiz_id=quiz_id
        )
        db.session.add(question)
        db.session.commit()
        flash('Question saved successfully!', 'success')
        return redirect(url_for('admin_manage_question', quiz_id=quiz_id))
    return render_template('/admin/add_question.html', form=form, quiz=quiz)


@app.route('/admin/edit_question/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_question(id):
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    question = Question.query.get_or_404(id)
    form = questionForm(obj=question)
    if form.validate_on_submit():
        question.statement = form.statement.data
        question.answer_1 = form.answer_1.data
        question.answer_2 = form.answer_2.data
        question.answer_3 = form.answer_3.data
        question.answer_4 = form.answer_4.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin_manage_question', quiz_id=question.quiz_id))
    return render_template('/admin/edit_question.html', form=form, question=question)


@app.route('/admin/delete_question/<int:id>', methods=['POST'])
@login_required
def admin_delete_question(id):
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin_manage_question', quiz_id=quiz_id))

# Take Quiz Get Result Route
@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    """take quiz route"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer == question.correct_option:
                score += 1
        user_result = Score(user_id=current_user.id, quiz_id=quiz_id, score=score)
        db.session.add(user_result)
        db.session.commit()
        flash(f'Quiz completed successfully! Your score is {score} out of {len(questions)}', 'success')
        return redirect(url_for('result', quiz_id=quiz_id))
    return render_template('take_quiz.html', quiz=quiz, questions=questions)


@app.route('/result/<int:quiz_id>', methods=['GET'])
@login_required
def result(quiz_id):
    """result route"""
    quiz = Quiz.query.get_or_404(quiz_id)
    score = Score.query.filter_by(quiz_id=quiz_id).all()
    return render_template('result.html', quiz=quiz, score=score)