# __init__.py
from flask import Flask, request, flash, redirect, render_template
from .extensions import db, login_manager, mail, csrf
from flask_migrate import Migrate
from app.blueprints.main import main_bp
from app.blueprints.auth import auth_bp
from app.blueprints.stories import stories_bp
from config import config_by_name
import sqlalchemy

def create_app(config_name='development'):  # Default to 'development' if no config specified
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(stories_bp, url_prefix='/stories')
    app.register_blueprint(main_bp, url_prefix='/')

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
