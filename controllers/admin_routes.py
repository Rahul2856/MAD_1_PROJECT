from app import app
from flask import render_template,request,redirect, url_for, flash
from controllers.rbac import adminlogin_required
from models import Subject ,db 

@adminlogin_required
@app.route("/admin_dashboard")
def admin_dashboard():
    subjects = Subject.query.all()  # This will return a list of all subjects

    return render_template("admin_templates/admin_dashboard.html", subjects=subjects)


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

@adminlogin_required
@app.route("/edit_subject/<int:subject_id>", methods=['GET','POST'])
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    # If the form is submitted (POST method)
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
      

        # Update the subject details
        subject.name = name
        db.session.commit()

        # Flash success message
        flash('Subject updated successfully!', 'success')

        # Redirect to the admin dashboard
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_templates/edit_subject.html',subject=subject)

@adminlogin_required
@app.route("/delete_subject/<int:subject_id>", methods=['POST'])
def delete_subject(subject_id):
    if request.method == 'POST':
        subject = Subject.query.get_or_404(subject_id)
        
        # Delete the subject
        db.session.delete(subject)
        db.session.commit()
        
        flash('Subject deleted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # This will only be reached if someone somehow sends a non-POST request
    flash('Invalid request method', 'error')
    return redirect(url_for('admin_dashboard'))





