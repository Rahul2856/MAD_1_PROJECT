from flask import Flask

app = Flask(__name__)

import config
import routes

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from dotenv import load_dotenv
# import os

# # ✅ Initialize database and login manager outside the function
# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app():
#     """Factory function to create and configure the Flask app."""
#     app = Flask(__name__)
#     load_dotenv()
#     app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#     app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
#         "SQLALCHEMY_TRACK_MODIFICATIONS"
#     )

#     # ✅ Ensure the database is properly initialized
#     db.init_app(app)

#     # ✅ Initialize Login Manager
#     login_manager = LoginManager()
#     login_manager.init_app(app)
#     login_manager.login_view = "auth.login"

#     @login_manager.user_loader
#     def load_user(user_id):
#         """Load user by ID for Flask-Login session handling"""
#         from app.models.model import User
#         return User.query.get(int(user_id))

#     # ✅ Import and register blueprints
#     from app.controllers.home import home_bp
#     from app.controllers.auth import auth_bp
#     from app.controllers.user_dashboard import user_dashboard_bp
#     from app.controllers.admin_dashboard import admin_bp
#     from app.controllers.quizzes import quizzes_bp

#     app.register_blueprint(home_bp, url_prefix="/")
#     app.register_blueprint(auth_bp, url_prefix="/auth")
#     app.register_blueprint(user_dashboard_bp, url_prefix="/dashboard")
#     app.register_blueprint(admin_bp, url_prefix="/admin")  # ✅ Ensure this matches admin_dashboard.py
#     app.register_blueprint(quizzes_bp, url_prefix="/quizzes")

#     return app  # ✅ Ensure the app instance is returned
