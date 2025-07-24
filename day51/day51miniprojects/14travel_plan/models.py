from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    plans = db.relationship('TravelPlan', backref='user', lazy=True)

class TravelPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(150), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
