from flask_testing import TestCase
from app import app, db, User
from sqlalchemy.exc import IntegrityError

class TestUserModel(TestCase):

    def create_app(self):
        # Configure your app for testing here
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(username='testuser').first())

    def test_unique_username(self):
        user1 = User(username='user1', email='user1@example.com', password='password')
        user2 = User(username='user1', email='user2@example.com', password='password')
        db.session.add(user1)
        db.session.commit()
    
        with self.assertRaises(IntegrityError):
            db.session.add(user2)
            db.session.commit()
    
    def test_unique_email(self):
        user1 = User(username='user1', email='test@example.com', password='password')
        user2 = User(username='user2', email='test@example.com', password='password')
        db.session.add(user1)
        db.session.commit()
      
        with self.assertRaises(IntegrityError):
            db.session.add(user2)
            db.session.commit()
    
    def test_user_creation_invalid_data(self):
        user = User(username=None, email='user@example.com', password='password')
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()