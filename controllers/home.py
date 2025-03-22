from flask import Blueprint, render_template
from app import app

@app.route("/")
def home():
    return render_template("index.html")  # ✅ Ensure the file exists inside `templates/`
