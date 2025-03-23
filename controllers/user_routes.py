from flask import render_template
from flask_login import login_required
from app import app


@app.route("/user_dashboard")
@login_required
def user_dashboard():
    return render_template("user_templates/user_dashboard.html")
