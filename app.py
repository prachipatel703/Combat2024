from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from celery import Celery

from forms import ReportForm, TaskForm, RegisterForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/db_name"
app.config["CELERY_BROKER_URL"] = "amqp://guest:guest@localhost"
app.config["CELERY_RESULT_BACKEND"] = "db+mysql://username:password@localhost/db_name"

db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="reports")
    image = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(64), nullable=False, default="open")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))
    report = db.relationship("Report", backref="tasks")
    collector_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    collector = db.relationship("User", backref="tasks")
    status = db.Column(db.String(64), nullable=False, default="open")


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/reports", methods=["GET", "POST"])
@login_required
def reports():
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(user_id=current_user.id, image=form.image.data, description=form.description.data,
                        location=form.location.data)
        db.session.add(report)
        db.session.commit()
        return redirect(url_for("reports"))
    reports = Report.query.all()
    return render_template("reports.html", form=form, reports=reports)


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(report_id=form.report_id.data, collector_id=form.collector_id.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("tasks"))
    tasks = Task.query.all()
    return render_template("tasks.html", form=form, tasks=tasks)


@app.route("/schedules", methods=["GET"])
@login_required
def schedules():
    schedules = Schedule.query.all()
    return render_template("schedules.html", schedules=schedules)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
