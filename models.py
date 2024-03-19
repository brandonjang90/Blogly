"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

DEFAULT_IMAGE_URL = "https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg"

class User(db.Model):
    """ Users """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    first_name = db.Column(db.Text, nullable=False) 
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ Posts """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref='posts')

    @property
    def friendly_created_at(self):
        return self.created_at.strftime("%B %d, %Y, %I:%M %p")
