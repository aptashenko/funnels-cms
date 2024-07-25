from datetime import datetime
from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    promocode_id = db.Column(db.String(20), nullable=True)
    web_user_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Promocodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), nullable=False)
    used = db.Column(db.Boolean, default=False)
    user_email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)