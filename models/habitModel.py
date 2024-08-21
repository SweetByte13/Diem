import uuid
from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

class Habit(db.Model, SerializerMixin):
    ___tablename__ = 'habits'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name=db.Column(db.String, nullable=False)
    color=db.Column(db.String, nullable=False)
    habit_tracking_type_id=db.Column(UUID(as_uuid=True), db.ForeignKey('habit_tracking_types.id'), nullable=False)
    recurrence_pattern=db.Column(db.String)
    created_dt=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    is_inactive=db.Column(db.Boolean)
    
    user_habits = db.relationship('User_Habit', back_populates='habit', cascade='all, delete-orphan')
    habit_occurances = db.relationship('Habit_Occurance', back_populates='habit', cascade='all, delete-orphan')
    habit_values= db.relationship('Habit_Value', back_populates='habit', cascade='all, delete-orphan')
    user=association_proxy('user_habits', 'user')
    habit_tracking_type=db.relationship('Habit_Tracking_Type', back_populates='habit')