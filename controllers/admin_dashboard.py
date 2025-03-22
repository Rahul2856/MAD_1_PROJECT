from flask import Blueprint, render_template,redirect,url_for,flash
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

@admin_bp.route("/admin_dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("user_dashboard.dashboard_page"))  # ✅ Prevent normal users from admin access
    return render_template("admin_dashboard.html", user=current_user)
