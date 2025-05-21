# tutorT/app/routes.py
from flask import render_template, current_app # current_app gives access to the app instance
# from app import app # This import might cause circular issues if app is not fully initialized.
                      # It's better to use blueprints or get app from current_app.

# Since 'app' is created in create_app, we can't directly import it at the top level here
# without causing circular dependencies if routes are imported during app creation.
# A common pattern is to define routes within a blueprint, or pass 'app' to a function that registers routes.

# For now, to make the import `from app import routes` in `__init__.py` work simply,
# let's assume `current_app` can be used or we define routes in a function called by `create_app`.

# A better way for now (before blueprints) is to register it within create_app
# Or to make `routes.py` define a blueprint.

# Let's modify this slightly for now.
# This will be directly imported and run by __init__.py

from flask import Blueprint, render_template
from flask_login import current_user # To use current_user in templates

# We will define a 'main' blueprint here shortly.
# For the absolute simplest start, and matching the `from app import routes` in __init__.py:

# If you want to keep `from app import routes` in `__init__.py` and have it work
# without blueprints for this very first step, you'd need `app` instance here.
# Let's assume routes are initialized after `app` is created and passed.
# So, the simplest route definition (will be refined):

# The `current_app` approach is cleaner if `routes.py` is imported by `__init__.py`

@current_app.route('/') # Using current_app.route decorator
@current_app.route('/index')
def index():
    # You might need to import current_user here if it's not globally available from Flask-Login context
    return render_template('index.html', title='Home')

# Let's refine this by creating a main blueprint immediately as it's better practice.

# Remove the @current_app.route above and use this blueprint approach:
# (You will need to adjust the import in `app/__init__.py` then)

bp = Blueprint('main', __name__) # Let's name it 'main'

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home Page', current_user=current_user)

# If you define `bp` like above, then in `app/__init__.py`:
# Remove `from app import routes`
# Add:
# from app.routes import bp as main_bp # or rename routes.py to main_routes.py
# app.register_blueprint(main_bp)