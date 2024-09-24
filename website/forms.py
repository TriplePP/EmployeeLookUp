from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Optional,
)


class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=30)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=30)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=7, max=30)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")


class UpdateUserForm(FlaskForm):
    email = StringField("Email", validators=[Optional(), Email()])
    first_name = StringField(
        "First Name", validators=[Optional(), Length(min=2, max=30)]
    )
    last_name = StringField("Last Name", validators=[Optional(), Length(min=2, max=30)])
    contact_number = StringField(
        "Contact Number", validators=[Optional(), Length(min=2, max=20)]
    )


class SearchUSerForm(FlaskForm):
    skill1 = StringField(validators=[Optional(), Length(min=2, max=30)])
    skill2 = StringField(validators=[Optional(), Length(min=2, max=30)])
    skill3 = StringField(validators=[Optional(), Length(min=2, max=30)])
