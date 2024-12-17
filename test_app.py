import pytest
from app import app, db
from flask import session
from werkzeug.security import generate_password_hash

# Pytest fixture for creating a test client without resetting the database
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False

    with app.test_client() as client:
        # The database should already have necessary tables, so no need to drop or recreate
        yield client

# Helper to login
def login(client, username, password):
    return client.post("/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)

# Helper to register user
def register(client, username, password, firstname, lastname):
    return client.post("/register", data={
        "username": username,
        "password": password,
        "firstname": firstname,
        "lastname": lastname
    }, follow_redirects=True)

# TEST CASES

def test_login_success(client):
    """Test user can log in successfully"""
    response = login(client, "testuser", "password")
    assert b"Home" in response.data  # Index page should show "Home" as title
    with client.session_transaction() as sess:
        assert "user_id" in sess  # User ID should exist in session

def test_login_invalid_username(client):
    """Test login with invalid username fails"""
    response = login(client, "wronguser", "password")
    assert b"Invalid username" in response.data

def test_login_invalid_password(client):
    """Test login with incorrect password fails"""
    response = login(client, "testuser", "wrongpassword")
    assert b"Invalid password" in response.data

def test_index_logged_out(client):
    """Test accessing home page redirects to login when not logged in"""
    response = client.get("/", follow_redirects=True)
    assert b"Login" in response.data

def test_register_duplicate_user(client):
    """Test registering an already existing username fails"""
    response = register(client, "testuser", "password", "test", "user")
    assert b"Username already exists" in response.data

def test_logout(client):
    """Test user logout functionality"""
    login(client, "testuser", "password")
    response = client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data  # Redirects back to login page
    with client.session_transaction() as sess:
        assert "user_id" not in sess  # User ID should be cleared from session

if __name__ == "__main__":
    pytest.main()







# def test_register_success(client):
#     """Test a new user registration process"""
#     response = register(client, "newuser", "newpassword", "first", "last")
#     assert b"Home" in response.data
#     with client.session_transaction() as sess:
#         assert "user_id" in sess  # User ID added to session



# def test_index_logged_in(client):
#     """Test accessing the home page while logged in"""
#     login(client, "testuser", "password")
#     response = client.get("/")
#     assert b"Net Worth" in response.data  # Check for expected content
#     assert b"Home" in response.data



# def test_calculate_stocks(client):
#     """Test the stock calculation function"""
#     # This test assumes that stocks are inserted in the existing database setup and we just test the result.
#     login(client, "testuser", "password")
#     response = client.get("/")
#     assert b"$500.00" in response.data  # 100 * 5 = 500

