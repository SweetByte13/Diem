from config import db, app
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID

class Habit_Value(db.Model, SerializerMixin):
    __tablename__= 'habit_values'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    habit_id=db.Column(UUID(as_uuid=True), ForeignKey='habit.id', default=uuid.uuid4, nullable=False)
    value=db.Column(db.String)  
    
    habit = db.relationship('Habit', back_populates='habit_values', cascade='all, delete-orphan')
    