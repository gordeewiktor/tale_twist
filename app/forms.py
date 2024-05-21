from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password (leave blank to keep current password)', validators=[Optional(), Length(min=6, max=128)])
    submit = SubmitField('Update Profile')


class CreateStoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    submit = SubmitField('Create Story')

class EditStoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    submit = SubmitField('Update Story')

class SegmentForm(FlaskForm):
    title = StringField('Segment Title', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    choice_text_1 = StringField('Choice 1 Text', validators=[Optional(), Length(max=100)])
    next_segment_id_1 = SelectField('Next Segment for Choice 1', coerce=lambda x: x if x == 'None' else int(x), choices=[], validate_choice=False)
    choice_text_2 = StringField('Choice 2 Text', validators=[Optional(), Length(max=100)])
    next_segment_id_2 = SelectField('Next Segment for Choice 2', coerce=lambda x: x if x == 'None' else int(x), choices=[], validate_choice=False)
    submit = SubmitField('Save Segment')

    def set_choices(self, segments, current_segment_id=None):
        # Exclude the current segment from choices to avoid self-looping
        segment_choices = [(str(seg.id), seg.title) for seg in segments if seg.id != current_segment_id]
        self.next_segment_id_1.choices = [('None', 'None')] + segment_choices  # 'None' option for no choice
        self.next_segment_id_2.choices = [('None', 'None')] + segment_choices




class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset Password')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

