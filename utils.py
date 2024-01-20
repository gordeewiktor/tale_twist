# utils.py
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app, url_for
from models import User

def get_reset_token(user_id, expires_sec=3600):  # Expires in one hour
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user_id}, salt='password-reset-salt')

def verify_reset_token(token, expiration=1800):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt='password-reset-salt', max_age=expiration)
        user_id = data['user_id']
    except:
        return None
    return User.query.get(user_id)

def send_reset_email(user_email, token):
    with current_app.app_context():
        msg = Message('Password Reset Request', sender='noreply@yourdomain.com', recipients=[user_email])
        msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
        current_app.mail.send(msg)
