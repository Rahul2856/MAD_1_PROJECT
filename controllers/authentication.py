from app import app
from models import User, db
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def home():
    return render_template("index.html")


# ✅ Login Route (Checks Admin & User)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User does not exist. Please register first!")
            return redirect(url_for("register"))  # Redirecting new user

        if not check_password_hash(user.password, password):
            flash("Incorrect Password.")
            return redirect(url_for("login"))  # Redirecting new user

        session["user_id"] = user.id
        session["username"] = user.username
        session["is_admin"] = user.is_admin

        if user.is_admin:
            return render_template("admin_templates/admin_dashboard.html")
        else:
            return render_template("user_templates/user_dashboard.html")

    return render_template("login.html")


# ✅ Register Route (Only for Normal Users)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            flash("Username already taken.")
            return redirect(url_for("register"))

        if existing_email:
            flash("Email is already registered before, try logging in instead.")
            return redirect(url_for("login"))

        # ✅ Hash the password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            full_name=full_name,
            email=email,
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ✅ Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
