# tutorT/run.py
from app import create_app, db # db is needed for shell context
from app.models import User # User model for shell context

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Makes variables accessible in the Flask shell without explicit imports.
    Run 'flask shell' to use.
    """
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run() # No need for debug=True here, FLASK_DEBUG in .flaskenv handles it