from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from website import bcrypt, db
from website.enums import JobRoles, Skills
from website.forms import RegistrationForm, LoginForm, UpdateUserForm, SearchUSerForm
from website.models import User, Job

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home", methods=["GET", "POST"])
@login_required
def home():
    form = UpdateUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        update_user(user)
    return render_template(
        "home.html",
        user=current_user,
        job_roles=JobRoles,
        jobs=Job.query.all(),
        is_home=True,
        skills=Skills,
        form=form,
    )


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered", "error")
            return redirect(url_for("main.register"))

        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=encrypted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash(
            "You have successfully registered! You can now log in", category="success"
        )
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            if check_password_hash(existing_user.password, form.password.data):
                login_user(existing_user)
                return redirect(url_for("main.home"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("Incorrect email", category="error")
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/view-record/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash(
            "Sorry you cannot delete your own account. Another admin will have to do this for you.",
            "error",
        )
        return redirect(url_for("main.view_record", user_id=user_id))
    else:
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted.", "success")
        return redirect(url_for("main.view_users"))


@main.route("/view-users", methods=["GET", "POST"])
def view_users():
    if not current_user.is_admin:
        flash("Please log in as an administrator to view this page", "error")
        return redirect(url_for("main.login"))
    return render_template("view-users.html", users=User.query.all())


@main.route("/search-users", methods=["GET", "POST"])
def search_users():
    form = SearchUSerForm()
    if not current_user.is_admin:
        flash("Please log in as an administrator to view this page", "error")
        return redirect(url_for("main.login"))
    # There is no form validation necessary here as the inputs are selection of set skill values which come from the Skills enum
    if request.method == "POST":
        # Using a ternary operator here to convert null values to empty strings
        skill_1 = request.form["skill_1"] if request.form["skill_1"] else ""
        skill_2 = request.form["skill_2"] if request.form["skill_2"] else ""
        skill_3 = request.form["skill_3"] if request.form["skill_3"] else ""
        filtered_users = []
        for user in User.query.all():
            # Converting the skills to empty strings means the __contains__ method below will still return true when no value is entered
            # This allows the user to leave empty fields in the search
            if (
                    user.__str__().__contains__(skill_1)
                    and user.__str__().__contains__(skill_2)
                    and user.__str__().__contains__(skill_3)
            ):
                filtered_users.append(user)
        if filtered_users.__len__() == 0:
            flash("Sorry there are no users with those skills", category="error")
        else:
            return render_template(
                "search-users.html", skills=Skills, users=filtered_users, form=form
            )
    return render_template("search-users.html", skills=Skills, form=form)


@main.route("/view-record/<int:user_id>/update", methods=["GET", "POST"])
def view_record(user_id: int):
    form = UpdateUserForm()
    user = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        update_user(user)
        return redirect(url_for("main.view_record", user_id=user_id))
    return render_template(
        "home.html",
        user=user,
        job_roles=JobRoles,
        jobs=Job.query.all(),
        is_home=False,
        skills=Skills,
        form=form,
    )

# function to update User record with input from HTML form on the home page
def update_user(user):
    user_fields = [
        "first_name",
        "last_name",
        "email",
        "contact_number",
        "skill_1",
        "skill_2",
        "skill_3",
    ]
    for field in user_fields:
        new_value = request.form[field]
        if new_value:
            setattr(user, field, new_value)
    job_title = request.form["job_title"]
    # We find the job id for the given job title and add this to our User record
    if job_title:
        job = Job.query.filter_by(job_title=job_title).first()
        job_id = job.id
        user.job_id = job_id
    db.session.commit()
