from website import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean, default=False)
    contact_number = db.Column(db.String(60), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120))
    department = db.Column(db.String(120))
    base_salary = db.Column(db.Integer)

from enum import Enum

class JobRoles(Enum):
    SOFTWARE_ENGINEER = "Software_Engineer"
    PRODUCT_MANAGER = "Product_Manager"
    SENIOR_SOFTWARE_ENGINEER = "Senior_Software_Engineer"
    TEAM_MANAGER = "Team_Manager"
    UX_DESIGNER = "UX_Designer"
    DATA_SCIENTIST = "Data_Scientist"
    CHIEF_TECHNOLOGY_OFFICER = "Chief_Technology_Officer"
    HUMAN_RESOURCES_MANAGER = "Human_Resources_Manager"
    MARKETING_DIRECTOR = "Marketing_Director"
    IT_SUPPORT_SPECIALIST = "IT_Support_Specialist"
    DATA_ANALYST = "Data_Analyst"




