from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import app

# ✅ Correctly initialize the database instance
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    scores = db.relationship("Score", backref="user", lazy=True)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    questions = db.relationship("Question", backref="quiz", lazy=True)
    scores = db.relationship("Score", backref="quiz", lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapters = db.relationship("Chapter", backref="subject", lazy=True)
    quizzes = db.relationship("Quiz", backref="subject", lazy=True) # Direct relationship


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    quizzes = db.relationship("Quiz", backref="chapter", lazy=True)


# Ensure all database operations run within an app context
with app.app_context():
    db.create_all()

    # Check if Admin already exists
    admin_user = User.query.filter_by(username="admin").first()  #
    if not admin_user:
        admin_user = User(
            username="admin",
            full_name="Administrator",
            password=generate_password_hash("admin"),
            is_admin=True,  # Mark as Admin
            email="admin@email.com",
        )
        db.session.add(admin_user)
        db.session.commit()

print("Database Setup Complete!")