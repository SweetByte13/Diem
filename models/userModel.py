import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from config import db, app
bcrypt = Bcrypt(app)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username=db.Column(db.String, nullable=False, unique=True)
    email=db.Column(db.String, nullable=False, unique=True)
    _password_hash=db.Column(db.String, nullable=False)
    
    user_habit = association_proxy('User_Habit', back_populate='user', cascade='all, delete-orphan')
    
