from config import db, app
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

class HabitOccurance(db.Model, SerializerMixin):
    __tablename__ = 'habit_occurances'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    habit_id=db.Column(UUID(as_uuid=True), db.ForeignKey('habit.id'), nullable=False)
    is_complete=db.Column(db.Boolean)
    dt_completed=db.Column(db.DateTime)
    due_date=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    habit_value_id=db.Column(UUID(as_uuid=True), db.ForeignKey('habit_values.id'))
    
    habit=db.relationship('Habit', back_populates='habit_occurances')
    habit_value=db.relationship('Habit_Value', back_populates='habit_occurances')