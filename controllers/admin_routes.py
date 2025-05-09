from app import app
from flask import render_template,request,redirect, url_for, flash
from controllers.rbac import adminlogin_required
from models import Subject ,db ,Chapter, Quiz, Question, Option

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


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        subject_id = request.form['subject_id']
        chapter_id = request.form['chapter_id']

        # Basic validation
        if not quiz_name or not subject_id or not chapter_id:
            flash('Please fill in all fields.', 'error')  
            return render_template('admin_templates/add_quiz.html', subjects=Subject.query.all(), chapters=Chapter.query.all())

        # Check if subject and chapter exist
        subject = Subject.query.get(subject_id)
        chapter = Chapter.query.get(chapter_id)
        if not subject or not chapter:
            flash('Invalid subject or chapter.', 'error')
            return render_template('admin_templates/add_quiz.html', subjects=Subject.query.all(), chapters=Chapter.query.all())

        # Create the new quiz
        new_quiz = Quiz(name=quiz_name, subject_id=subject_id, chapter_id=chapter_id)
        db.session.add(new_quiz)
        db.session.commit()

        flash('Quiz added successfully!', 'success')  
        return redirect(url_for('quiz_management'))  # Redirect to quiz management page

    # If it's a GET request, just render the form
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    return render_template('admin_templates/add_quiz.html', subjects=subjects, chapters=chapters)

@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)  # Get the quiz to edit

    if request.method == 'POST':
        # Get data from the form
        quiz.name = request.form['quiz_name']
        subject_id = request.form['subject_id']
        chapter_id = request.form['chapter_id']

        # Basic validation
        if not quiz.name or not subject_id or not chapter_id:
            flash('Please fill in all fields.', 'error')
            subjects = Subject.query.all()
            chapters = Chapter.query.all()
            return render_template('admin_templates/edit_quiz.html', quiz=quiz, subjects=subjects, chapters=chapters)

        # Check if subject and chapter exist
        subject = Subject.query.get(subject_id)
        chapter = Chapter.query.get(chapter_id)
        if not subject or not chapter:
            flash('Invalid subject or chapter.', 'error')
            subjects = Subject.query.all()
            chapters = Chapter.query.all()
            return render_template('admin_templates/edit_quiz.html', quiz=quiz, subjects=subjects, chapters=chapters)

        # Update the quiz
        quiz.subject_id = subject_id
        quiz.chapter_id = chapter_id
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('quiz_management'))  # Redirect to quiz management

    # If it's a GET request, render the form with the quiz data
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    return render_template('admin_templates/edit_quiz.html', quiz=quiz, subjects=subjects, chapters=chapters)


@app.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapters = Chapter.query.all()

    if request.method == 'POST':
        question_title = request.form['question_title']
        question_statement = request.form['question_statement']
        option1_text = request.form['option1']
        option2_text = request.form['option2']
        option3_text = request.form['option3']
        option4_text = request.form['option4']
        correct_option = request.form['correct_option']  # Get the selected option

        # Basic validation (add more as needed)
        if not question_statement or not question_title or not correct_option:
            flash('Please fill in all required fields.', 'error')
            return render_template('admin_templates/add_question.html', quiz=quiz, chapters=chapters)

        # Create the new question
        new_question = Question(question_title=question_title, question_statement=question_statement, quiz_id=quiz_id) # Added chapter_id
        db.session.add(new_question)
        db.session.flush()  # To get the new question's ID

        # Create the options and set is_correct
        options_data = [
            {'text': option1_text, 'value': 'option1'},
            {'text': option2_text, 'value': 'option2'},
            {'text': option3_text, 'value': 'option3'},
            {'text': option4_text, 'value': 'option4'},
        ]

        for option_data in options_data:
            is_correct = (option_data['value'] == correct_option)
            option = Option(question_id=new_question.id, option_text=option_data['text'], is_correct=is_correct)
            db.session.add(option)

        db.session.commit()

        flash('Question and options added successfully!', 'success')
        return redirect(url_for('quiz_management'))

    return render_template('admin_templates/add_question.html', quiz=quiz, chapters=chapters)


