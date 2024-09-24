from flask_bcrypt import generate_password_hash

from website import create_app, db
from website.models import User

app = create_app()
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(email="admin@example.com").first()

    if admin is None:
        admin = User(
            first_name="admin",
            last_name="user",
            email="admin@example.com",
            password=generate_password_hash("password").decode("utf-8"),
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
        print("Successfully created admin profile")
    else:
        print("Admin profile already exists")
