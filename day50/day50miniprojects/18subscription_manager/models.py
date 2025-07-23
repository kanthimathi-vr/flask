from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    plan = db.Column(db.String(50), nullable=False)
    subscribed_on = db.Column(db.DateTime, default=datetime.utcnow)
