from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)  # ✅ Ensure Blueprint is named correctly

# 🏠 User Dashboard Route
@dashboard_bp.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', user=current_user)

# 🏠 Admin Dashboard Route
@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':  # Check if the user is admin
        return render_template('unauthorized.html'), 403
    return render_template('admin_dashboard.html', user=current_user)
