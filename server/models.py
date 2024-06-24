from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(200))
    bio = db.Column(db.String(200))


    @hybrid_property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username must be provided')
        return username



class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.String(1000), nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)


    user = db.relationship('User', backref=db.backref('recipes', lazy=True))

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title must be provided')
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters long')
        return instructions
