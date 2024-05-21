from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db, login_manager
from app.models import User
from app.forms import RegistrationForm, LoginForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app.utils import send_reset_email, verify_reset_token

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already in use. Please use a different email.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        print("Hashed Attemted password:", hashed_password)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print("DB Hashed Password:", user.password)  # Print the hashed password from the database
            print("Attempted Password:", form.password.data)  # Print the password attempt
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.home'))
        flash('Invalid email or password.', 'danger')
    else:
        if form.errors:
            print("Form Errors:", form.errors)  # Print form errors if there are any
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        print("Form is validated")
        existing_user = User.query.filter(User.id != current_user.id, (User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already taken.', 'danger')
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.new_password.data:
                current_user.password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main.home'))  # Redirect to home page
    else:
        print("Form validation failed")
        print(form.errors)
    return render_template('profile.html', form=form)


@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Check your email for the instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = verify_reset_token(token)
    if not user:
        flash('The token is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
