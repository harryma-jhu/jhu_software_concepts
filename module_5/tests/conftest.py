import pytest
from src import create_app
# Created separate conftest.py file to hold the client fixture that can be used across multiple test files in the tests directory. 
# This allows us to avoid repeating the same code to create a test client in each test file, and makes it easier to maintain and 
# update the test setup in one place if needed.
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client