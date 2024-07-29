from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        """Set the user's password hash."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the user's password hash."""
        return check_password_hash(self.password, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(150))
    title = db.Column(db.String(150))
    subtitle = db.Column(db.String(150))
    content = db.Column(db.String(200))
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relación con User

    @classmethod
    def get_all_posts(cls):
        return cls.query.all()

    @classmethod
    def get_posts_by_section(cls, section):
        return cls.query.filter_by(section=section).all()

class MemorySection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sectionName = db.Column(db.String(150))
    memories = db.relationship('Memory', backref='section', lazy=True)  # Relación con Memory

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120))
    file_type = db.Column(db.String(10))
    section_id = db.Column(db.Integer, db.ForeignKey('memory_section.id'))  # Relación con MemorySection
