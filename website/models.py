from .init import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from flask_login import login_user, login_required, logout_user, current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150))
    role = db.Column(db.String(80), nullable=False, default='student')
