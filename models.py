from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

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
    type

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)