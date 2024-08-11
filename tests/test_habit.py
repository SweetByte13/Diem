import pytest
import uuid
from faker import Faker
from app import app
from config import db
from models.habitModel import Habit
from models.userModel import User

@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client

class TestHabit:
    def test_create_habit(self, client):
        '''creates oa habit with a POST request to /habit.'''
        name = "test habit"
        color = "#32a852"
        habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
        recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th;"
        habit_values = ["Cardio", "Weights"]

        user = User.query.first()
        response = client.post(
            '/habit',
            json={
                'name': name,
                'color': color,
                'habit_tracking_type_id': habit_tracking_type_id,
                'recurrence_pattern': recurrence_pattern,
                'user_id': user.id,
                'habit_values': habit_values
            }
        ).json

        habit = Habit.query.filter(
            Habit.id == uuid.UUID(response['id'])).one_or_none()
        assert habit
        
        db.session.delete(habit)
        db.session.commit()

    def test_create_habit_bad_rrule(self, client):
        '''POST request to /habit throws an error when an invalid rrule is passed.'''
        name = "test habit"
        color = "#32a852"
        habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
        recurrence_pattern = "FREQ=Gochujung;BYDAY=Tu,Th;"
        habit_values = ["Cardio", "Weights"]

        response = client.post(
            '/habit',
            json={
                'name': name,
                'color': color,
                'habit_tracking_type_id': habit_tracking_type_id,
                'recurrence_pattern': recurrence_pattern,
                'habit_values': habit_values
            }
        )
        assert response.status_code != 200

    def test_create_habit_bad_color(self, client):
        '''POST request to /habit throws an error when an invalid hex color is passed.'''
        name = "test habit"
        color = "#Gochujubng32a852"
        habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
        recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th;"
        habit_values = ["Cardio", "Weights"]

        response = client.post(
            '/habit',
            json={
                'name': name,
                'color': color,
                'habit_tracking_type_id': habit_tracking_type_id,
                'recurrence_pattern': recurrence_pattern,
                'habit_values': habit_values
            }
        )
        assert response.status_code != 200
        