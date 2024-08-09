from config import db, app
import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID


class Habit_Tracking_Type(db.Model, SerializerMixin):
    __tablename__ = 'habit_tracking_types'
    
    id=db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name=db.Column(db.String, nullable=False)

    habit = db.relationship('Habit', back_populates='habit_tracking_types')