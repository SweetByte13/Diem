import pytest
import uuid
from faker import Faker
from app import app
from config import db
from models.habitModel import Habit
from models.habitOccuranceModel import Habit_Occurance
from models.userHabitModel import User_Habit
from models.userModel import User
from models.habitValueModel import Habit_Value
from datetime import datetime, timedelta, timezone
from controllers.habits import HabitById

@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client

class TestHabit:
    def test_create_habit(self, client):
        '''creates a habit with a POST request to /habit.'''
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
        print(response)
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
 
    #test for marking habit inactive
    def test_patch_route(self, client):
        '''updates a habit with a PATCH request to /habits/<id>.'''
        
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

        patch_data = {
            "name": "Updated Habit",
            "is_inactive": True
        }
        
        response = client.patch(f'/habits/{str(habit.id)}', json=patch_data)

        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

        updated_habit = Habit.query.get(habit.id)
        assert updated_habit.name == "Updated Habit"
        assert updated_habit.is_inactive

        db.session.delete(habit)
        db.session.commit()
    
    def test_mark_habit_occurance_complete(self, client):
        '''marks habit occurance complete with a patch request to /mark_habit_occurance_complete.'''

        name = "test habit"
        color = "#32a852"
        habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
        recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th;"
        two_week_ago = datetime.now() - timedelta(weeks=2)

        user = User.query.first()

        habit = Habit(
                name=name,
                color=color,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type_id),
                recurrence_pattern = recurrence_pattern,
                created_dt = two_week_ago
            )
        
        habit_occurance = Habit_Occurance()
        habit.habit_occurances.append(habit_occurance)
        
        new_user_habit = User_Habit()
        new_user_habit.habit = habit
        user.user_habits.append(new_user_habit) 
        db.session.commit()

        response = client.patch(
            f'/mark_habit_occurance_complete/{habit_occurance.id}'
        )

        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

        habit_occurance_new = Habit_Occurance.query.filter(
            Habit_Occurance.id == habit_occurance.id).one_or_none()
        
        assert habit_occurance_new
        assert habit_occurance_new.is_complete == True
        
        db.session.delete(habit_occurance)
        db.session.delete(habit)
        db.session.commit()

    def test_mark_habit_occurance_incomplete(self, client):
        '''marks habit occurance incomplete with a patch request to /mark_habit_occurance_complete.'''

        name = "test habit"
        color = "#32a852"
        habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
        recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th;"
        two_week_ago = datetime.now() - timedelta(weeks=2)

        user = User.query.first()

        habit = Habit(
                name=name,
                color=color,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type_id),
                recurrence_pattern = recurrence_pattern,
                created_dt = two_week_ago
            )
        
        habit_occurance = Habit_Occurance(
            is_complete=True,
            dt_completed=datetime.now(timezone.utc)
        )
        habit.habit_occurances.append(habit_occurance)
        
        new_user_habit = User_Habit()
        new_user_habit.habit = habit
        user.user_habits.append(new_user_habit) 
        db.session.commit()

        response = client.patch(
            f'/mark_habit_occurance_incomplete/{habit_occurance.id}'
        )

        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

        habit_occurance_new = Habit_Occurance.query.filter(
            Habit_Occurance.id == habit_occurance.id).one_or_none()
        
        assert habit_occurance_new
        assert habit_occurance_new.is_complete == False
        
        db.session.delete(habit_occurance)
        db.session.delete(habit)
        db.session.commit()

def test_delete_habit(client):
    '''Deletes a habit and its dependencies with a DELETE request to /habit/<id>.'''

    # Create a habit with dependencies
    name = "test habit2"
    color = "#32a851"
    habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
    recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th,Sa;"
    habit_values = ["Walking", "Lifting"]

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
    )
    print(f"POST response status: {response.status_code}")
    print(f"POST response data: {response.json}")

    # Ensure the habit was created successfully
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    habit_response = response.json
    created_habit_id = habit_response['id']
    assert created_habit_id, "No ID returned for the created habit"

    # Retrieve the habit from the database
    habit = Habit.query.filter(Habit.id == uuid.UUID(created_habit_id)).one_or_none()
    assert habit, f"Habit with ID {created_habit_id} was not found in the database"

  # Verify habit and dependencies are added 
    print("Verifying habit and dependencies...") 
    habit_values_in_db = db.session.query(Habit_Value).filter(Habit_Value.habit_id == habit.id).all() 
    print(f"Habit Values in DB: {habit_values_in_db}") 
    assert db.session.query(Habit).filter(Habit.id == habit.id).one_or_none() is not None 
    assert len(habit_values_in_db) == len(habit_values), f"Expected {len(habit_values)} habit values, found {len(habit_values_in_db)}" 
    assert db.session.query(User_Habit).filter(User_Habit.habit_id == habit.id).one_or_none() is not None
    
    # Delete the habit using the delete method from HabitById class
    habit_by_id = HabitById()
    habit_by_id.delete(habit.id)

    # Verify habit and dependencies are deleted
    assert db.session.query(Habit).filter(Habit.id == habit.id).one_or_none() is None
    assert db.session.query(Habit_Value).filter(Habit_Value.habit_id == habit.id).one_or_none() is None
    assert db.session.query(User_Habit).filter(User_Habit.habit_id == habit.id).one_or_none() is None

    # Cleanup: Ensure no leftover data
    db.session.query(Habit_Value).filter(Habit_Value.habit_id == habit.id).delete()
    db.session.query(User_Habit).filter(User_Habit.habit_id == habit.id).delete()
    db.session.query(Habit).filter(Habit.id == habit.id).delete()
    db.session.commit()
