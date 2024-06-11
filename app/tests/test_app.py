import pytest
from app import create_app, db
from app.models import User, Story, Segment, Choice
from flask import url_for
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def new_app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def init_database(new_app):
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture
def client(new_app):
    return new_app.test_client()

def test_add_segment(client, init_database):
    # Create a test user and story
    hashed_password = generate_password_hash('testpass', method='pbkdf2:sha256')
    user = User(username='testuser', email='test@example.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    story = Story(title='Test Story', description='A test story', genre='test', author=user)
    db.session.add(story)
    db.session.commit()
    
    # Log in the user
    login_response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    print("Login Response Data:", login_response.data)
    assert login_response.status_code == 302, f"Login failed: {login_response.data}"

def test_edit_segment(client, init_database):
    # Create a test user, story, and segment
    hashed_password = generate_password_hash('testpass2', method='pbkdf2:sha256')
    user = User(username='testuser2', email='test2@example.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    story = Story(title='Test Story 2', description='A second test story', genre='test', author=user)
    db.session.add(story)
    db.session.commit()
    
    segment = Segment(story_id=story.id, title='Original Segment', content='Original content')
    db.session.add(segment)
    db.session.commit()
    
    # Log in the user
    login_response = client.post('/auth/login', data={
        'email': 'test2@example.com',
        'password': 'testpass2'
    })
    print("Login Response Data:", login_response.data)
    assert login_response.status_code == 302, f"Login failed: {login_response.data}"
