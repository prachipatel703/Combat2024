from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    role = StringField("Role", validators=[DataRequired()])
    submit = SubmitField("Register")

class ReportForm(FlaskForm):
    image = FileField("Image", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField("Submit")

class TaskForm(FlaskForm):
    report_id = StringField("Report ID", validators=[DataRequired()])
    collector_id = StringField("Collector ID", validators=[DataRequired()])
    submit = SubmitField("Assign")