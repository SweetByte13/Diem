from config import db, app
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class HabitOccurance(db.Model, SerializerMixin):
    __tablename__ = 'habit_occurances'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    habit_id=db.Column(UUID(as_uuid=True), ForeignKey='habit.id', nullable=False)
    is_complete=db.Column(db.Boolean)
    dt_completed=db.Column(db.db.DateTime, default=datetime.utcnow)
    due_date=db.Column(db.db.DateTime, nullable=False, default=datetime.utcnow)
    habit_value_id=db.Column(UUID(as_uuid=True), ForeignKey='habit_value.id', default=uuid.uuid4)
    
    habit=db.relationship('Habit', back_populates='user_habit')
    habit_value=db.relationship('Habit_Value', back_populates='habit_value')