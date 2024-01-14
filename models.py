from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app import bcrypt
import hashlib

metadata = MetaData(naming_convention={
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
})

db = SQLAlchemy(metadata=metadata)

def hash_email(email):
    hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
    return hashed_email

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    hashed_email = db.Column(db.String, nullable=False)

    def set_email(self, email):
        self.hashed_email = hash_email(email)

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate_password(self,password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    def authenticate_email(self, email):
        hashed_email = hash_email(email)
        return self.hashed_email == hashed_email
    
class Meme(db.Model, SerializerMixin):
    __tablename__ = 'memes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Cart_items(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))

    meme_id = db.Column(db.Integer, db.ForeignKey('memes.id'), nullable=False)
    meme = db.relationship('Meme', backref=db.backref('cart_items', lazy=True))
