from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import bcrypt, db
from app.forms import RegistrationForm
from app.models import User

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template("home.html")


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
            flash('You have successfully registered!', category='success')
            return redirect(url_for('main.home'))
    return render_template("register.html", form=form)


@main.route('/login')
def login():
    return render_template("login.html")


@main.route('/logout')
def logout():
    return render_template("register.html")
