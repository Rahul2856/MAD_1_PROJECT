from app import create_app, db
from app.models.user import User
from app.models.quiz import Quiz, Question

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database Created Successfully!")
