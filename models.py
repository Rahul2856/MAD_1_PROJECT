from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import app

# ✅ Correctly initialize the database instance
db = SQLAlchemy(app)  


class User(db.Model):  # ✅ Make sure db.Model is used correctly
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)

    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # One-to-Many: A subject has many chapters
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    # One-to-Many: A chapter has many quizzes
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)


#Ensure all database operations run within an app context
with app.app_context():
    db.create_all()

    #Check if Admin already exists
    admin_user = User.query.filter_by(username="admin@example.com").first() #
    if not admin_user:
        admin_user = User(
            username="admin@example.com",
            full_name="Administrator",
            password=generate_password_hash("admin"),
            is_admin=True  #Mark as Admin
        )
        db.session.add(admin_user)
        db.session.commit()

print("Database Setup Complete!")
   


