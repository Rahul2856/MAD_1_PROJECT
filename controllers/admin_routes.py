from app import app
from flask import render_template,request,redirect, url_for, flash
from controllers.rbac import adminlogin_required
from models import Subject ,db ,Chapter, Quiz

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



#section for add/edit/delete of chapters

@adminlogin_required
@app.route("/add_chapter/<int:subject_id>",methods=['GET','POST'])
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        # Get chapter name and description from the form
        chapter_name = request.form.get("chapter_name")
        chapter_description = request.form.get("description")

         
        if not chapter_name:
            flash("Chapter name is required!", "error")
            return redirect(url_for("add_chapter", subject_id=subject.id))
        
        new_chapter = Chapter(
        name=chapter_name,
        description=chapter_description,  
        subject_id=subject.id
        )

        db.session.add(new_chapter)
        db.session.commit()

        flash("Chapter added successfully!", "success")
        return redirect(url_for("add_chapter", subject_id=subject.id))
    
    return render_template('admin_templates/add_chapter.html',subject=subject)

@app.route("/edit_chapter/<int:chapter_id>", methods=["GET", "POST"])
@adminlogin_required
def edit_chapter(chapter_id):
   
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == "POST":
      
        chapter_name = request.form.get("chapter_name")
        chapter_description = request.form.get("description")
        
        # Update chapter details
        chapter.name = chapter_name
        chapter.description = chapter_description
        db.session.commit()  # Save changes to the database

        # Flash success message
        flash("Chapter updated successfully!", "success")

        # Redirect back to the subject's edit page
        return redirect(url_for("edit_chapter", chapter_id=chapter.id))

    # Render the edit chapter form
    return render_template("admin_templates/edit_chapter.html", chapter=chapter)


@app.route("/delete_chapter/<int:chapter_id>", methods=["POST"])
@adminlogin_required
def delete_chapter(chapter_id):
    # Find the chapter by ID
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # Delete the chapter
    db.session.delete(chapter)
    db.session.commit()

    # Flash success message
    flash("Chapter deleted successfully!", "success")

    # Redirect back to the subject's edit page
    return redirect(url_for("admin_dashboard", subject_id=chapter.subject_id))


#section for add/edit/delete of quizzes

@app.route("/quiz_management", methods=["GET", "POST"]) 
@adminlogin_required
def quiz_management():
    quizzes = Quiz.query.all()
    chapter = Subject.query.all()
    return render_template("admin_templates/quiz_management.html", quizzes=quizzes, chapter=chapter)



# @app.route("/add_quiz/<int:chapter_id>", methods=["GET", "POST"])
# @adminlogin_required
# def add_quiz(chapter_id):
    
#     chapter = Chapter.query.get_or_404(chapter_id)

#     # Handle POST request (when the form is submitted)
#     if request.method == "POST":
#         quiz_title = request.form.get("quiz_title")

#         # If quiz title is provided
#         if quiz_title:
#             # Create a new Quiz instance
#             new_quiz = Quiz(
#                 title=quiz_title,
#                 chapter_id=chapter.id  # Associate quiz with the chapter
#             )
#             # Add the new quiz to the database session
#             db.session.add(new_quiz)
#             db.session.commit()  # Commit to the database
         
#             flash("Quiz added successfully!", "success")            
   
#             return redirect(url_for("add_quiz", chapter_id=chapter.id))

#     # Render the add_quiz form
#     return render_template("admin_templates/add_quiz.html", chapter=chapter)


# @app.route("/add_quiz/<int:chapter_id>", methods=["GET", "POST"])
# @adminlogin_required
# def add_quiz(chapter_id):
#     chapter = Chapter.query.get_or_404(chapter_id)

#     if request.method == "POST":
#         quiz_title = request.form.get("quiz_title")

#         if quiz_title:
#             # Create a new quiz under the chapter
#             new_quiz = Quiz(
#                 title=quiz_title,
#                 chapter_id=chapter.id
#             )
#             db.session.add(new_quiz)
#             db.session.commit()

#             flash("Quiz added successfully!", "success")
#             return redirect(url_for("edit_chapter", chapter_id=chapter.id))

#     return render_template("admin_templates/add_quiz.html", chapter=chapter)
