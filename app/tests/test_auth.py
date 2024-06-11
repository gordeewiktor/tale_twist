# app/tests/test_auth.py

import pytest
from app import create_app, db
from app.models import User

@pytest.fixture(scope='module')
def new_app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(new_app):
    return new_app.test_client()

@pytest.fixture(scope='module')
def init_database(new_app):
    db.create_all()
    yield db
    db.drop_all()

def test_register(client, init_database):
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 302  # Redirect after successful registration

    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.username == 'testuser'

def test_login(client, init_database):
    client.post('/auth/register', data={
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    response = client.post('/auth/login', data={
        'email': 'testuser2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirect after successful login
