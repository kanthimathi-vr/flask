from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Attendee(db.Model):
    __tablename__ = 'attendees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    event_name = db.Column(db.String(150), nullable=False)
