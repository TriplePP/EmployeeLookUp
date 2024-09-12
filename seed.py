from website import create_app, db
from website.models import Job

app = create_app()
with app.app_context():
    db.create_all()
    db.session.commit()
