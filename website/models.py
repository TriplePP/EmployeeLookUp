from datetime import datetime
from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(60))
    # is_admin = db.Column(db.Boolean, default=False)
    # contact_number = db.Column(db.String(60), nullable=True)
    # address = db.Column(db.String(300), nullable=True)
    # skills = db.Column(db.ARRAY(db.String), nullable=True)
    # job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)


# class Job(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     job_title = db.Column(db.String(120))
#     department = db.Column(db.String(60))
#     base_salary = db.Column(db.Integer)
