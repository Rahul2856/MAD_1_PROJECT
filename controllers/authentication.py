from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

# # ✅ Login Route (Checks Admin & User)
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         flash("You are already logged in.", "info")
#         return redirect(url_for("dashboard.user_dashboard"))  # ✅ Prevent multiple logins

#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         user = User.query.filter_by(username=username).first()

#         if not user:
#             flash("User does not exist. Please register first!", "warning")
#             return redirect(url_for("auth.register"))  # ✅ Redirecting new user

#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             flash("Login successful!", "success")

#             if user.is_admin:
#                 return redirect(url_for("admin_dashboard.dashboard_page"))
#             else:
#                 return redirect(url_for("dashboard.user_dashboard"))
#         else:
#             flash("Invalid username or password. Try again.", "danger")

#     return render_template("login.html")

# ✅ Register Route (Only for Normal Users)
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if current_user.is_authenticated:
#         flash("You are already logged in.", "info")
#         return redirect(url_for("dashboard.user_dashboard"))

#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         full_name = request.form["full_name"]

#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash("Username already taken! Try another.", "danger")
#             return redirect(url_for("auth.register"))
        
#         # ✅ Hash the password and create a new user
#         hashed_password = generate_password_hash(password, method="sha256")
#         new_user = User(username=username, password=hashed_password, full_name=full_name, )  
#         db.session.add(new_user)
#         db.session.commit()

#         flash("Registration successful! You can now log in.", "success")
#         return redirect(url_for("auth.login"))

#     return render_template("register.html")


# ✅ Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()  
    flash("You have been logged out.", "info")  
    return redirect(url_for("auth.login"))  
