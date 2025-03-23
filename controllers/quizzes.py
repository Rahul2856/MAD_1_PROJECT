# from flask import Blueprint, render_template, request
# from flask_login import login_required
# from app.models.model import Quiz, Question
# from app import db

# # ✅ Initialize Blueprint
# quizzes_bp = Blueprint('quizzes', __name__)

# # 🟢 Route to List All Quizzes
# @quizzes_bp.route('/quizzes')
# @login_required
# def list_quizzes():
#     quizzes = Quiz.query.all()
#     return render_template('quizzes.html', quizzes=quizzes)

# # 🔵 Route to View a Specific Quiz
# @quizzes_bp.route('/quiz/<int:quiz_id>')
# @login_required
# def view_quiz(quiz_id):
#     quiz = Quiz.query.get_or_404(quiz_id)
#     return render_template('quiz_detail.html', quiz=quiz, questions=quiz.questions)
