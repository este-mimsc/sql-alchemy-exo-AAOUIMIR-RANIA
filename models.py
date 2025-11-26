"""Database models for the blog assignment."""
from app import db  

class User(db.Model):
    """Represents a user who can author posts."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {getattr(self, 'username', None)}>"

class Post(db.Model):
    """Represents a blog post written by a user."""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Add a relationship to allow passing user object directly
    user = db.relationship("User", foreign_keys=[user_id], overlaps="posts,author")

    def __repr__(self):
        return f"<Post {getattr(self, 'title', None)}>"
