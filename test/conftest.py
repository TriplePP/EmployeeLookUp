import pytest
from flask_bcrypt import generate_password_hash

from config import TestConfig
from website import create_app, db


@pytest.fixture(scope="function")
def app():
    flask_app = create_app(config_class=TestConfig)

    yield flask_app  # Yield the app for the test



@pytest.fixture(scope="function")
def test_client(app):
    testing_client = app.test_client()

    with app.app_context():
        yield testing_client


@pytest.fixture(scope="function")
def init_database(app):
    with app.app_context():
        from website.models import User, Job

        db.create_all()
        admin = User.query.filter_by(email="admin@example.com").first()

        # create a test user
        admin = User(
            first_name="admin",
            last_name="user",
            email="admin@example.com",
            password=generate_password_hash("password").decode("utf-8"),
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
        #create a test job
        test_job = Job(job_title="test tile", department="test department", base_salary=70000)
        db.session.add(test_job)
        db.session.commit()
        yield db  # This is where the testing happens!

        # Drop the database and the tables
        db.drop_all()

# We to create a user and log them in for home page to function correctly
def login_user(test_client):
    return test_client.post('/login', data=dict(
        email='admin@example.com',
        password='password'
    ), follow_redirects=True)
