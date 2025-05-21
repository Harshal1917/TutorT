# tutorT/app/models.py
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login # db from app/__init__.py

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Flask-Login user loader function
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id)) # Changed from User.query.get for SQLAlchemy 2.0 compatibility


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True, index=True) # e.g., 'Programming', 'Science', 'Arts'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Relationship to Resource: A subject can have many resources
    resources = db.relationship('Resource', backref='subject', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Subject {self.name}>'


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False) # e.g., 'text', 'video_link', 'pdf'
    content = db.Column(db.Text, nullable=True) # For text content or embed codes
    url = db.Column(db.String(500), nullable=True) # For links or file paths
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Optional: if you want to track who added it

    def __repr__(self):
        return f'<Resource {self.title}>'