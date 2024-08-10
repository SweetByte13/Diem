import pytest
from app import app


@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client

class TestHome:
    def test_hello_world(self, client):
        '''makes sure the apps base root functions and returns "Hello World!"'''
        response = client.get("/")
        assert response.status_code == 200
        response = response.json
        assert response == "Hello World!"

