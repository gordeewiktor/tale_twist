# routes.py
from flask import render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from flask import current_app as app
from extensions import db
from models import User, Story, Segment, Choice
from forms import RegistrationForm, LoginForm, EditProfileForm
from utils import get_reset_token, verify_reset_token, send_reset_email
from werkzeug.security import check_password_hash
from extensions import login_manager

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_routes(app):

    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already in use. Please use a different email.', 'danger')
                return redirect(url_for('register'))

            # No existing user with this email, so create a new user
            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=form.role.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))

        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))  # Redirect to 'home'
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title="Login", form=form)
    
    @app.route('/logout', methods=['GET'])
    def logout():
        logout_user()  # This will log out the current user
        return redirect(url_for('home'))
    
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)

    
    @app.route('/edit_profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm(obj=current_user)
        if form.validate_on_submit():
            existing_user = User.query.filter(User.id != current_user.id, ((User.username == form.username.data) | (User.email == form.email.data))).first()
            if existing_user:
                flash('Username or email already taken.', 'danger')
            else:
                current_user.username = form.username.data
                current_user.email = form.email.data
                if form.new_password.data:
                    current_user.password = generate_password_hash(form.new_password.data)
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile'))

        return render_template('edit_profile.html', form=form)
    
    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        user = verify_reset_token(token)
        if not user:
            flash('This is an invalid or expired token', 'warning')
            return redirect(url_for('login'))
    
        if request.method == 'POST':
            new_password = request.form['password']
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
    
        return render_template('reset_password.html', token=token)
    
    @app.route('/reset_password_request', methods=['GET', 'POST'])
    def reset_password_request():
        if request.method == 'POST':
            email = request.form['email']
            user = User.query.filter_by(email=email).first()
            if user:
                token = get_reset_token(user.id)
                send_reset_email(user.email, token)
                flash('Check your email for the instructions to reset your password', 'info')
            else:
                flash('Email not found', 'error')
        return render_template('reset_password_request.html')
    
    # Functional routes ////////////////////////////////////////////////////
    # Writing routes
    
    @app.route('/create_story', methods=['GET', 'POST'])
    @login_required
    def create_story():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            genre = request.form['genre']
            new_story = Story(title=title, description=description, author=current_user, genre=genre)
            db.session.add(new_story)
            db.session.commit()
            flash('Story created successfully!', 'success')
            return redirect(url_for('edit_story', story_id=new_story.id))
        return render_template('create_story.html')
    
    @app.route('/edit_story/<int:story_id>', methods=['GET', 'POST'])
    @login_required
    def edit_story(story_id):
        story = Story.query.get_or_404(story_id)
        if current_user != story.author:
            flash('You can only edit your own stories.', 'danger')
            return redirect(url_for('home'))
        if request.method == 'POST':
            story.title = request.form['title']
            story.description = request.form['description']
            story.genre = request.form['genre']
            db.session.commit()
            flash('Story updated successfully!', 'success')
            return redirect(url_for('view_story', story_id=story.id))
        return render_template('edit_story.html', story=story)

    @app.route('/create_segment/<int:story_id>', methods=['GET', 'POST'])
    @login_required
    def create_segment(story_id):
        story = Story.query.get_or_404(story_id)
        if current_user != story.author:
            flash('You are not authorized to add segments to this story.', 'danger')
            return redirect(url_for('home'))
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_segment = Segment(story_id=story.id, title=title, content=content)
            db.session.add(new_segment)
            db.session.commit()
            flash('Segment added successfully!', 'success')
            return redirect(url_for('edit_story', story_id=story.id))
        return render_template('create_segment.html', story=story)


  
    @app.route('/edit_segment/<int:segment_id>', methods=['GET', 'POST'])
    def edit_segment(segment_id):
        segment = Segment.query.get_or_404(segment_id)
        if request.method == 'POST':
            if current_user != segment.story.author:
                flash('You are not authorized to edit this segment.', 'danger')
                return redirect(url_for('home'))
            segment.content = request.form['segment_content']
            db.session.commit()
            flash('Segment updated successfully!', 'success')
            return redirect(url_for('edit_story', story_id=segment.story_id))
        return render_template('edit_segment.html', segment=segment)

    @app.route('/add_choices/<int:segment_id>', methods=['POST'])
    @login_required
    def add_choices(segment_id):
        segment = Segment.query.get_or_404(segment_id)
        # Ensure the current user is the author of the story
        if current_user.id != segment.story.author_id:
            flash('You are not authorized to add choices to this segment.', 'danger')
            return redirect(url_for('home'))

        # Get form data for both choices
        choice_text_1 = request.form['choice_text_1']
        next_segment_id_1 = int(request.form['next_segment_id_1'])
        choice_text_2 = request.form['choice_text_2']
        next_segment_id_2 = int(request.form['next_segment_id_2'])

        # Create new choices and add them to the database
        choice1 = Choice(segment_id=segment_id, text=choice_text_1, next_segment_id=next_segment_id_1)
        choice2 = Choice(segment_id=segment_id, text=choice_text_2, next_segment_id=next_segment_id_2)
        db.session.add(choice1)
        db.session.add(choice2)
        db.session.commit()

        flash('Choices added successfully!', 'success')
        return redirect(url_for('edit_story', story_id=segment.story.id))

    
    @app.route('/delete_segment/<int:segment_id>', methods=['GET'])
    @login_required
    def delete_segment(segment_id):
        segment = Segment.query.get_or_404(segment_id)
        if segment.story.author != current_user:
            flash('You can only delete segments from your own stories.', 'danger')
            return redirect(url_for('home'))
    
        db.session.delete(segment)
        db.session.commit()
    
        flash('Segment deleted successfully!', 'success')
        return redirect(url_for('edit_story', story_id=segment.story.id))
    
    @app.route('/reorder_segment/<int:story_id>', methods=['POST'])
    @login_required
    def reorder_segment(story_id):
        story = Story.query.get_or_404(story_id)
        if story.author != current_user:
            return jsonify({"error": "You are not authorized to reorder segments in this story"}), 403
    
        new_order = request.json.get('order', [])
        for index, segment_id in enumerate(new_order):
            segment = Segment.query.get(segment_id)
            if segment and segment.story_id == story_id:
                segment.order = index
            else:
                return jsonify({"error": "Invalid segment or segment does not belong to the story"}), 400
    
        db.session.commit()
        return jsonify({"message": "Segments reordered successfully"})

    
      # Reading routes
    
    @app.route('/stories')
    def stories():
        all_stories = Story.query.all()
        return render_template('stories.html', stories=all_stories)

    
    @app.route('/read_story/<int:story_id>/<int:segment_id>')
    def read_story(story_id, segment_id):
        story = Story.query.get_or_404(story_id)
        segment = Segment.query.get_or_404(segment_id)
        return render_template('read_story.html', story=story, segment=segment)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback the database session in case of database errors
        return render_template('500.html'), 500