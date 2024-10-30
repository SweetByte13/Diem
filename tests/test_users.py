import pytest
from faker import Faker
from app import app
from config import db
from models.habitOccuranceModel import Habit_Occurance
from models.userModel import User
from models.userHabitModel import User_Habit
from models.habitModel import Habit
from datetime import datetime, timedelta
import uuid


@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client

class TestUsers:
    def test_sign_up(self, client):
        '''creates one user using a username, email, and password with a POST request to /signup.'''
        fake = Faker()
        username = fake.user_name()
        email = fake.email()
        password = fake.name_nonbinary() + '!'
        response = client.post(
            '/signup',
            json={
                'username': username,
                'email': email,
                'password':password
            }
        ).json

        assert response['id']
        assert response['username'] == username
        assert response['email'] == email
        assert response['created_dt']

        user = User.query.filter(
            User.username == username, User.email == email).one_or_none()
        assert user
        
        db.session.delete(user)
        db.session.commit()
            

    def test_login_correct_password(self, client):
        '''logs a user in with the correct username and password'''
        with app.app_context():
            fake = Faker()
            password = fake.password()
            user = User(
                username=fake.user_name(), email=fake.email())
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            response = client.post(
                '/login',
                json={
                    'username': user.username,
                    'password': password
                }
            )
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            assert response['username'] == user.username
            assert response['email'] == user.email

            db.session.delete(user)
            db.session.commit()

    def test_login_incorrect_password(self, client):
        '''attempts to log a user in with an incorrect password'''
        with app.app_context():
            fake = Faker()
            password = fake.password()
            user = User(
                username=fake.user_name(), email=fake.email())
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            response = client.post(
                '/login',
                json={
                    'username': user.username,
                    'password': 'wrongpassword'
                }
            )
            assert response.status_code == 401
            assert response.content_type == 'application/json'
            response = response.json

            assert 'Error' in response
            assert response['Error'] == 'Invalid password'

            db.session.delete(user)
            db.session.commit()
            
    def test_logout(self, client):
        '''logs a user out with a DELETE request to /logout'''
        with app.app_context():
            fake = Faker()
            password = fake.password()
            user = User(
                username=fake.user_name(), email=fake.email())
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            response = client.post(
                '/login',
                json={
                    'username': user.username,
                    'password': password
                }
            )
            assert response.status_code == 200

            response = client.delete('/logout')
            assert response.status_code == 204

            db.session.delete(user)
            db.session.commit()

    def test_get_habits_by_user_and_date_range(self, client):
        '''gets habits for a user by id and date range.'''

        fake = Faker()
        username = fake.user_name()
        email = fake.email()
        password = fake.name_nonbinary() + '!'
        response = client.post(
            '/signup',
            json={
                'username': username,
                'email': email,
                'password':password
            }
        ).json

        user_id =  response['id']
        user = db.session.get(User, uuid.UUID(user_id))

        name = "zzzz test habit"
        color = "#32a852"
        habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
        recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th;"

        two_week_ago = datetime.now() - timedelta(weeks=2)
        one_week_ago = datetime.now() - timedelta(weeks=1)

        habit = Habit(
                name=name,
                color=color,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type_id),
                recurrence_pattern = recurrence_pattern,
                created_dt = two_week_ago
            )
        
        new_user_habit = User_Habit()
        new_user_habit.habit = habit
        user.user_habits.append(new_user_habit) 

        db.session.commit()

        response = client.post(
            f'/habits_by_user/{user.id}',
            json={
                'startDate': one_week_ago.strftime("%Y-%m-%d"),
                'endDate': datetime.now().strftime("%Y-%m-%d")
            }
        )
        
        assert response.status_code == 200

        response_json = response.json
        
        habit_response = next(i for i in response_json if i["name"] == "zzzz test habit")

        assert habit_response
        assert len(habit_response["habit_occurances"]) == 2

        Habit_Occurance.query.filter_by(habit_id=habit.id).delete()
        
        db.session.delete(habit)
        db.session.delete(user)
        db.session.commit()