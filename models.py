from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Integer

DATABASE_URL = 'postgresql:///blogly_users_db'

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

engine = create_engine(DATABASE_URL)

# Models
class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)
    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=True)
    image_url = db.Column(db.String(255),
                          nullable=True,
                          unique=False,
                          default='/static/default_icon.png')
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
