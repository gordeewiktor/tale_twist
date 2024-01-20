# app.py
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os
from extensions import db, login_manager, mail, csrf


app = Flask(__name__)

# Logging setup
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/yourapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('YourApp startup')

# Configuration settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true') == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@example.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-email-password')

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
csrf.init_app(app)

# Additional Flask-Login setup
login_manager.login_view = 'login'  # Redirect to login page if not logged in

# Import routes
from routes import register_routes
register_routes(app)

with app.app_context():
  db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)