# Choosit - Quiz Management System

A comprehensive quiz management system built with Flask that allows users to create, take, and manage quizzes with subject-based organization and user administration.

## 📚 Project Overview

**Choosit** is an interactive quiz platform featuring:

- User registration & login
- Session-based quiz solving
- Score tracking and result review
- Admin dashboard for managing subjects, quizzes, questions, scores, and users

It demonstrates core backend engineering principles like routing, ORM with SQLAlchemy, dynamic templating, form validation, and user authentication.
---

## 🚀 Features

- User Authentication & Authorization
  - User registration and login
  - Role-based access control (Admin/User)
- Quiz Management
  - Create and manage quizzes
  - Subject-based organization
  - Question management with multiple choice answers
- Quiz Taking
  - Interactive quiz interface
  - Score tracking
  - Result display
- Admin Dashboard
  - User management
  - Subject management
  - Quiz administration
  - Question management

## 🛠️ Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/MOSALAHDEV/choosit-app.git
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Configure your environment variables in `.env`

5. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
choosit/
├── app/
│   ├── templates/
│   │   ├── base.html          # Base template
│   │   ├── dashboard.html     # User dashboard
│   │   ├── result.html        # Quiz result display
│   │   ├── take_quiz.html     # Quiz taking interface
│   │   ├── login.html         # Login page
│   │   ├── register.html      # Registration page
│   │   └── admin/
│   │       ├── dashboard.html      # Admin dashboard
│   │       ├── manage_subject.html # Subject management
│   │       ├── manage_quizzes.html # Quiz management
│   │       ├── manage_questions.html # Question management
│   │       └── manage_users.html    # User management
│   ├── models/
│   │   ├── user.py         # User model
│   │   ├── quiz.py         # Quiz model
│   │   ├── question.py     # Question model
│   │   ├── score.py        # Score model
│   │   └── subject.py      # Subject model
│   ├── forms.py            # Form definitions
│   └── routes.py           # Application routes
├── instance/
│   └── choosit.db          # SQLite database
├── run.py                  # Application entry point
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## � Dependencies

- Flask 3.1.1
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Flask-WTF 1.2.2
- SQLAlchemy 2.0.41
- Other Python packages as listed in requirements.txt
