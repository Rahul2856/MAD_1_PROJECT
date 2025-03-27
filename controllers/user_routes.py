from flask import render_template
from controllers.rbac import userlogin_required
from app import app


@app.route("/user_dashboard")
@userlogin_required
def user_dashboard():
    return render_template("user_templates/user_dashboard.html")
