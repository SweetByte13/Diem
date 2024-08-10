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
        username = "TestUsername"
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
            

