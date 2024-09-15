import json
from dataclasses import fields
from time import process_time_ns

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_

from website import bcrypt, db
from website.enums import JobRoles, Skills
from website.forms import RegistrationForm, LoginForm
from website.models import User, Job

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        user = User.query.filter_by(id=current_user.id).first()
        update_user(user)
        return redirect(url_for('main.home'))
    return render_template("home.html",
                           user=current_user,
                           job_roles=JobRoles,
                           jobs=Job.query.all(),
                           is_home=True,
                           skills=Skills)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.is_submitted():
            existing_user = User.query.filter_by(email=form.email.data).first()
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
def view_users():
    if not current_user.is_admin:
        flash('Please log in as an administrator to view this page', 'error')
        return redirect(url_for('main.login'))
    return render_template('view-users.html', users=User.query.all())


@main.route('/search-users', methods=['GET', 'POST'])
def search_users():
    if not current_user.is_admin:
        flash('Please log in as an administrator to view this page', 'error')
        return redirect(url_for('main.login'))
    if request.method == "POST":
        skill_1 = request.form['skill_1'] if request.form['skill_1'] else ''
        skill_2 = request.form['skill_2'] if request.form['skill_2'] else ''
        skill_3 = request.form['skill_3'] if request.form['skill_3'] else ''
        filtered_users = []
        for user in User.query.all():
            if (user.__str__().__contains__(skill_1) and
                    user.__str__().__contains__(skill_2) and
                    user.__str__().__contains__(skill_3)):
                print(user)
                filtered_users.append(user)
        if filtered_users.__len__() == 0:
            flash('Sorry there are no users with those skills', category='error')
        else:
            return render_template('search-users.html', skills=Skills, users=filtered_users)
    return render_template('search-users.html', skills=Skills)


@main.route('/view-record/<int:user_id>/update', methods=['GET', 'POST'])
def view_record(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        update_user(user)
        return redirect(url_for('main.view_record', user_id=user_id))
    return render_template("home.html",
                           user=user,
                           job_roles=JobRoles,
                           jobs=Job.query.all(),
                           is_home=False,
                           skills=Skills)


def update_user(user):
    user_fields = ['first_name', 'last_name', 'email', 'contact_number', 'skill_1', 'skill_2', 'skill_3']
    for field in user_fields:
        new_value = request.form[field]
        if new_value:
            setattr(user, field, new_value)
    job_title = request.form['job_title']
    if job_title:
        job = Job.query.filter_by(job_title=job_title).first()
        job_id = job.id
        user.job_id = job_id
    db.session.commit()
