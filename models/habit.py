from config import db, app
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID

class Habit(db.Model, SerializerMixin):
    ___tablename__ = 'habits'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=db.Column(db.String, nullable=False)
    color=db.Column(db.String, nullable=False)
    habit_type_id=db.Column(UUID(as_uuid=True), ForeignKey='habit_type', default=uuid.uuid4, nullable=False)
    recurrence_pattern=db.Column(db.String)
    
    user_habit = association_proxy('User_Habit', back_populate='habit', cascade='all, delete-orphan')