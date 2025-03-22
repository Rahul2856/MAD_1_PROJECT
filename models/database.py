from app import create_app , db
from app.models.model import User  # Import User model
from werkzeug.security import generate_password_hash

# ✅ Create Flask app instance
app = create_app()

# ✅ Ensure all database operations run within an app context
with app.app_context():
    print("🔄 Setting up the database...")

    
    # ✅ Create database tables if they do not exist
    db.create_all()

    # ✅ Check if Admin already exists
    admin_user = User.query.filter_by(username="admin@example.com").first()
    if not admin_user:
        admin_user = User(
            username="admin@example.com",  # ✅ Keep it consistent with login
            full_name="Administrator",
            password=generate_password_hash("adminpassword"),
            is_admin=True  # ✅ Mark as Admin
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created successfully!")
    else:
        print("⚠️ Admin user already exists.")

print("✅ Database Setup Complete!")
