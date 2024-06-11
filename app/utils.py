from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app, url_for

def send_reset_email(user_email, token):
    msg = Message('Password Reset Request',
                  sender='noreply@example.com',
                  recipients=[user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, max_age=3600)['user_id']
    except:
        return None
    from app.models import User
    return User.query.get(user_id)
