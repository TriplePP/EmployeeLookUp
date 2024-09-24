from sqlalchemy.ext.declarative import declarative_base

from website import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    skill_1 = db.Column(db.String(60), nullable=True)
    skill_2 = db.Column(db.String(60), nullable=True)
    skill_3 = db.Column(db.String(60), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    contact_number = db.Column(db.String(60), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=True)

    job = db.relationship("Job")

    # This string representation was created for the search_users function. So only skills were needed.
    def __repr__(self):
        return f"{self.id}, {self.skill_1}, {self.skill_2}, {self.skill_3}"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120))
    department = db.Column(db.String(120))
    base_salary = db.Column(db.Integer)
