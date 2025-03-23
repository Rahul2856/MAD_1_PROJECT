from app import app
from flask import render_template,request,redirect, url_for
from controllers.rbac import adminlogin_required
from models import Subject ,db

@adminlogin_required
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_templates/admin_dashboard.html")


@adminlogin_required
@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        subject_name = request.form.get("subject_name")

        if subject_name:
            # Create a new subject and add it to the database
            new_subject = Subject(name=subject_name)
            db.session.add(new_subject)
            db.session.commit()

            # Redirect to the subjects list (or any other page, such as the dashboard)
            return redirect(url_for("add_subject"))

    return render_template("admin_templates/add_subject.html")
