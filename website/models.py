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
    image = db.Column(db.String(255))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer) 
    level = db.Column(db.String(50))  
    price = db.Column(db.Float) 
    language = db.Column(db.String(50))
    tags = db.Column(db.String(100))
    documents = db.relationship('Document', backref='course', lazy=True)
    videos = db.relationship('Video', backref='course', lazy=True)
    owner = db.relationship('User', backref=db.backref('courses', lazy=True))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)