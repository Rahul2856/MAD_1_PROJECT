# from flask import Blueprint, render_template,redirect,url_for
# from flask_login import login_required, current_user

# user_dashboard_bp = Blueprint('user_dashboard', __name__,template_folder="../templates")  

# user_dashboard_bp.route("/dashboard")
# @login_required
# def user_dashboard():
#     if current_user.is_admin:
#         return redirect(url_for("admin_dashboard.admin_dashboard"))  # ✅ Restrict admin users
#     return render_template("user_dashboard.html")

