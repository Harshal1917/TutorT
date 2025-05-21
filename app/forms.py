from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField # Added PasswordField and BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User # We'll use this later to check if username/email already exists

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # These are custom validators we'll implement later or you can add now
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SubjectForm(FlaskForm):
    title = StringField('Subject Title',
                        validators=[DataRequired(), Length(min=3, max=150)])
    content = TextAreaField('Text Content',
                            validators=[Length(max=10000)])


class ResourceForm(FlaskForm):
    title = StringField('Resource Title',
                        validators=[DataRequired(), Length(min=3, max=150)])
    resource_type = SelectField('Resource Type', 
                                choices=[
                                    ('text', 'Text Content'),
                                    ('video_link', 'Video Link'),
                                    ('external_link', 'External Link'),
                                    ('pdf', 'PDF Document'), # We'll handle file upload logic later
                                    ('embed', 'Embed Code (e.g., YouTube Iframe)')
                                ],
                                validators=[DataRequired()])
    content = TextAreaField('Text Content / Embed Code', 
                            validators=[Length(max=10000)]) # Optional, used for 'text' or 'embed'
    url = StringField('URL (for Video/External Link/PDF)',
                      validators=[Length(max=500)]) # Optional, used for link types
    # subject_id will be handled in the route, not directly in the form by the user.
    submit = SubmitField('Save Resource')