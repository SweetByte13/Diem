import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from config import db, app
import re
bcrypt = Bcrypt(app)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username=db.Column(db.String(30), nullable=False, unique=True)
    email=db.Column(db.String, nullable=False, unique=True)
    _password_hash=db.Column(db.String, nullable=False)
    
    user_habit = association_proxy('User_Habit', back_populate='user', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.CheckConstraint('length(username)>5 AND length(username)>30', name='username_length'),
        db.CheckConstraint("username NOT LIKE '%[^a-zA-Z0-9_]%'", name='username_no_special_chars')
    )

    @validates('username')
    def validates_username(self, key, new_username):
        if not new_username:
            raise AssertionError ("Username is required")
        if len(new_username)<5:
            raise AssertionError ("Username must be longer than 5 characters")
        if User.query.filter_by(username = new_username):
            raise AssertionError ("Username is already taken")
        if not re.match("^[a-zA-Z0-9_]+$", new_username):
            raise ValueError("Username must not contain special characters.")
        return new_username