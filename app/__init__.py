# app/__init__.py
from flask import Flask, request, flash, redirect, render_template, jsonify, Blueprint, send_from_directory
from .extensions import db, login_manager, mail, csrf
from flask_migrate import Migrate
from app.blueprints.main import main_bp
from app.blueprints.auth import auth_bp
from app.blueprints.stories import stories_bp
from app.models import Story, User
from config import config_by_name
import sqlalchemy
import os
from werkzeug.security import generate_password_hash

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/stories', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    stories_data = [{'id': story.id, 'title': story.title, 'description': story.description} for story in stories]
    return jsonify(stories_data)

@api_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    errors = {}
    if User.query.filter_by(username=username).first():
        errors['username'] = 'That username is already taken. Please choose a different one.'
    if User.query.filter_by(email=email).first():
        errors['email'] = 'That email is already in use. Please choose a different one.'
    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    if errors:
        return jsonify({'errors': errors}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful!'}), 201

def create_app(config_name='production'):  # Use 'production' if deploying to production
    app = Flask(__name__, static_folder='../frontend/build')
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(stories_bp, url_prefix='/stories')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')

    # Serve React frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # Define the global error handler for SQLAlchemy IntegrityError
    @app.errorhandler(sqlalchemy.exc.IntegrityError)
    def handle_integrity_error(e):
        db.session.rollback()
        flash('A database error occurred. Please check your inputs.', 'danger')
        return redirect(request.url)

    # Define error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    # Define error handler for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app
