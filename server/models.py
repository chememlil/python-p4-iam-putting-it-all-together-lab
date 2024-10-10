from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    _password_hash = Column('password_hash', String, nullable=False)
    image_url = Column(String)
    bio = Column(String)

    @hybrid_property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be provided")
        return username

    recipes = relationship('Recipe', back_populates='user')


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    minutes_to_complete = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='recipes')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must be provided")
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long")
        return instructions
