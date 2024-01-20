# models.py
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)


  def __init__(self, username, email, password):
    if not username or not username.strip():
        raise ValueError("Username cannot be empty or blank")
    if not email or not email.strip():
        raise ValueError("Email cannot be empty or blank")
    if not password or not password.strip():
        raise ValueError("Password cannot be empty or blank")
    self.username = username
    self.email = email
    self.password = generate_password_hash(password)  # Hash the password
  def __repr__(self):
      return f'<User {self.username}>'

class Story(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  author = db.relationship('User')
  genre = db.Column(db.String(50), nullable=False)
  creation_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
  def __init__(self, title, description, author, genre):
    self.title = title
    self.description = description
    self.author = author
    self.genre = genre

class Segment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
  title = db.Column(db.String(100), nullable=False)  # Added title field
  content = db.Column(db.Text, nullable=False)
  choices = db.relationship('Choice', backref='segment', lazy='dynamic')

  def __init__(self, story_id, title, content):
      self.story_id = story_id
      self.title = title
      self.content = content


class Choice(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'), nullable=False)
  next_segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'))
  text = db.Column(db.String(100), nullable=False)
