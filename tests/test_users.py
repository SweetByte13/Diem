import pytest
from faker import Faker
from app import app
from config import db
from models.userModel import User


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