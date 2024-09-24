import pytest
from flask_bcrypt import generate_password_hash

from config import TestConfig
from website import create_app, db


# Create the Flask app fixture
@pytest.fixture(scope="module")
def app():
    # Create an instance of the Flask app
    flask_app = create_app(config_class=TestConfig)

    yield flask_app  # Yield the app for the test


# Create the test client fixture that depends on the app fixture
@pytest.fixture(scope="module")
def test_client(app):
    # Create a test client using the Flask app instance
    testing_client = app.test_client()

    # Establish an application context before running the tests
    with app.app_context():
        yield testing_client  # This is where the testing happens!


# Create the init_database fixture that also depends on the app fixture
@pytest.fixture(scope="module")
def init_database(app):
    # Create the database and the tables
    with app.app_context():
        from website.models import User, Job

        db.create_all()
        admin = User.query.filter_by(email="admin@example.com").first()

        if admin is None:
            admin = User(
                first_name="admin",
                last_name="user",
                email="admin@example.com",
                password=generate_password_hash("password").decode("utf-8"),
                is_admin=True,
            )
            db.session.add(admin)
            db.session.commit()

        test_job = Job(job_title="test tile", department="test department", base_salary=70000)
        db.session.add(test_job)
        db.session.commit()
        yield db  # This is where the testing happens!

        # Drop the database and the tables
        db.drop_all()
