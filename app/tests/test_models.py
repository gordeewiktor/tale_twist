# app/tests/test_models.py

import pytest
from app import create_app, db
from app.models import Story, Segment, Choice, User

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

def test_choice_with_none_next_segment(init_database):
    # Create a test user, story, and segments
    user = User(username='testuser', email='test@example.com', password='testpass')
    db.session.add(user)
    db.session.commit()

    story = Story(title='Test Story', description='A test story', genre='test', author=user)
    db.session.add(story)
    db.session.commit()

    segment1 = Segment(story_id=story.id, title='Segment 1', content='First segment')
    segment2 = Segment(story_id=story.id, title='Segment 2', content='Second segment')
    db.session.add(segment1)
    db.session.add(segment2)
    db.session.commit()

    # Create a choice with next_segment_id set to None
    choice1 = Choice(segment_id=segment1.id, text='Choice 1', next_segment_id=None)
    db.session.add(choice1)
    db.session.commit()

    # Assert that the choice is correctly saved with next_segment_id as None
    assert choice1.next_segment_id is None
    assert choice1.next_segment is None

    # Create a choice with next_segment_id pointing to another segment
    choice2 = Choice(segment_id=segment1.id, text='Choice 2', next_segment_id=segment2.id)
    db.session.add(choice2)
    db.session.commit()

    # Assert that the choice is correctly saved with a valid next_segment_id
    assert choice2.next_segment_id == segment2.id
    assert choice2.next_segment == segment2
