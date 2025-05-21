from flask import render_template, url_for, flash, redirect, request, Blueprint # Added Blueprint here
from app import db
from app.forms import RegistrationForm, LoginForm # Import LoginForm
from app.models import User # Make sure User is imported
from flask_login import login_required # Make sure login_required is imported
from werkzeug.security import generate_password_hash

from flask_login import current_user, login_user, logout_user, login_required # Import login_user, logout_user, login_required

bp = Blueprint('main', __name__) # Naming the blueprint 'main'

@bp.route('/') # Changed from @main.route to @bp.route
@bp.route('/index') # Changed from @main.route to @bp.route
def index():
    return render_template('index.html', title='Home')

@bp.route('/register', methods=['GET', 'POST']) # Changed from @main.route to @bp.route
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user_by_username = User.query.filter_by(username=form.username.data).first()
        if existing_user_by_username:
            flash('That username is already taken. Please choose a different one.', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        existing_user_by_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_by_email:
            flash('That email address is already registered. Please choose a different one or login.', 'danger')
            return render_template('register.html', title='Register', form=form)

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('main.login')) # Assuming login route is also on 'main' blueprint
    return render_template('register.html', title='Register', form=form)

# Add this new placeholder login route:
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Redirect if already logged in
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next') # For redirecting after login if 'next' param exists
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout') # Changed from @main.route to @bp.route
@login_required # Ensures only logged-in users can access this
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title=f"{user.username}'s Profile", user=user)