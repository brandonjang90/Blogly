"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

DEFAULT_IMAGE_URL = ""

class User(db.Model):
    """ Users """
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                     nullable=False)
    
    last_name = db.Column(db.Text,
                     nullable=False)
    
    image_url = db.Column(db.Text,
                       nullable=False,
                       default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name."""

        return f"{self.first_name} {self.last_name}"

