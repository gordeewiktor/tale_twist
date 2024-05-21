from app.extensions import db
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    stories = db.relationship('Story', backref='author', lazy=True)  # Relationship to the Story model

    def __init__(self, username, email, password):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty or blank")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty or blank")
        if not password or not password.strip():
            raise ValueError("Password cannot be empty or blank")
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    segments = db.relationship('Segment', backref='story', lazy=True)  # Relationship to the Segment model

    def __repr__(self):
        return f'<Story {self.title}>'

class Segment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    choices = db.relationship('Choice', backref='origin_segment', lazy='dynamic', foreign_keys='Choice.segment_id')

    def __repr__(self):
        return f'<Segment {self.title}>'

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    next_segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'), nullable=True)
    next_segment = db.relationship('Segment', foreign_keys=[next_segment_id], remote_side=[Segment.id], post_update=True)

    def __repr__(self):
        return f'<Choice {self.text}>'
