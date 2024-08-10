import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from datetime import datetime, timezone
from config import db
import re
# from app import bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    username=db.Column(db.String(30), nullable=False, unique=True)
    email=db.Column(db.String, nullable=False, unique=True)
    created_dt=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    _password_hash=db.Column(db.String, nullable=False)
    
    user_habits = db.relationship('User_Habit', back_populates='user', cascade='all, delete-orphan')
    habits = association_proxy('user_habits', 'habit')
    
    __table_args__ = (
        db.CheckConstraint('length(username)>5 AND length(username)<30', name='username_length'),
        db.CheckConstraint("username NOT LIKE '%[^a-zA-Z0-9_]%'", name='username_no_special_chars')
    )

    @property
    def password_hash(self):
        return self._password_hash 
    
    @password_hash.setter
    def password_hash(self, password):
        from app import bcrypt 
        passHash = bcrypt.generate_password_hash(password)
        self._password_hash = passHash.decode('utf-8')
        
    def authenticate(self, password):
        from app import bcrypt 
        return bcrypt.check_password_hash(self._password_hash, password)
    
    @validates('username')
    def validates_username(self, key, new_username):
        if not new_username:
            raise AssertionError ("Username is required")
        if len(new_username)<5:
            raise AssertionError ("Username must be longer than 5 characters")
        if User.query.filter_by(username = new_username).first():
            raise AssertionError ("Username is already taken")
        if not re.match("^[a-zA-Z0-9_]+$", new_username):
            raise ValueError("Username must not contain special characters.")
        return new_username
    