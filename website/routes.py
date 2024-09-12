import json

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from website import bcrypt, db
from website.forms import RegistrationForm, LoginForm
from website.models import User, Job, JobRoles

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        user = User.query.filter_by(id=current_user.id).first()
        update_user(user)
        return redirect(url_for('main.home'))
    return render_template("home.html", user=current_user, job_roles=JobRoles, jobs=Job.query.all(), is_home=True)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.is_submitted():
            existing_user = User.query.filter_by(email=form.email.data).first()
            job_title = request.form['job_title']
            job = Job.query.filter_by(title=job_title).first()
            job_id = job.id
            if existing_user:
                flash('Email already registered', 'error')
                return redirect(url_for('main.register'))

            encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=encrypted_password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered! You can now log in', category='success')
            return redirect(url_for('main.login'))
    return render_template("register.html", form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.is_submitted():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                if check_password_hash(existing_user.password, form.password.data):
                    login_user(existing_user)
                    flash('You have successfully logged in', category='success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Incorrect password', category='error')
            else:
                flash('Incorrect email', category='error')
    return render_template("login.html", form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# The create job and delete job routes were created to add and delete jobs via the command line.
# They are not for the user.
@main.route('/create-job', methods=['POST'])
def create_job():
    data = request.get_json()
    job_title = data['job_title']
    department = data['department']
    base_salary = data['base_salary']
    new_job = Job(job_title=job_title, department=department, base_salary=base_salary)
    db.session.add(new_job)
    db.session.commit()
    print("Successfully added entries")
    return "added"


@main.route('/delete-job', methods=['DELETE'])
def delete_job():
    data = request.get_json()
    job_title = data['job_title']
    job = Job.query.filter_by(job_title=job_title).first()
    if job:
        db.session.delete(job)
        db.session.commit()
        return f"{job_title} deleted", 200
    else:
        return "Job not found", 404


@main.route('/view-users', methods=['GET', 'POST'])
def admin_tasks():
    if not current_user.is_admin:
        flash('Please log in as an administrator to view this page', 'error')
        return redirect(url_for('main.login'))

    return render_template('view-users.html', users=User.query.all())


@main.route('/view-record/<int:user_id>/update', methods=['GET', 'POST'])
def view_record(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        update_user(user)
        return redirect(url_for('main.view_record', user_id=user_id))
    return render_template("home.html", user=user, job_roles=JobRoles, jobs=Job.query.all(), is_home=False)


def update_user(user):
    print(user)
    print("TEST")
    print(request)
    print(request.form)
    print(request.form['last_name'])
    new_first_name = request.form['first_name']
    new_last_name = request.form['last_name']
    new_email = request.form['email']
    new_contact_number = request.form['contact_number']
    job_title = request.form['job_title']
    if new_first_name:
        user.first_name = new_first_name
    if new_last_name:
        user.last_name = new_last_name
    if new_email:
        user.email = new_email
    if new_contact_number:
        user.contact_number = new_contact_number
    if job_title:
        job = Job.query.filter_by(job_title=job_title).first()
        job_id = job.id
        user.job_id = job_id
    db.session.commit()