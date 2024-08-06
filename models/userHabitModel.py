from config import db, app
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import UUID

class User_Habit(db.Model, SerializerMixin):
    __tablename__ = 'user_habits'
    
    user_id=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False, default=uuid.uuid4)
    habit_id=db.Column(UUID(as_uuid=True), db.ForeignKey('habit.id'), nullable=False, default=uuid.uuid4)
    
    user=db.relationship('User', back_populates='user_habits')
    habit=db.relationship('Habit', back_populates='user_habits')