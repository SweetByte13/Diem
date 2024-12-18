from config import db
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID

class Habit_Value(db.Model, SerializerMixin):
    __tablename__= 'habit_values'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    habit_id=db.Column(UUID(as_uuid=True), db.ForeignKey('habit.id'), nullable=False,)
    value=db.Column(db.String, nullable=False)  
    
    habit = db.relationship('Habit', back_populates='habit_values')
    habit_occurances = db.relationship('Habit_Occurance', back_populates='habit_value', cascade='all, delete-orphan')