from test.conftest import test_client, login_user


def test_register(test_client):
    """
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_login(test_client):
    """
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Log in" in response.data


def test_user_redirect(test_client):
    """
    WHEN the logged out user requests('/home') (GET)
    THEN check the user is redirected to login page
    """
    response = test_client.get('/home', follow_redirects=True)
    assert b"Log in" in response.data


def test_home(test_client, init_database):
    """
    WHEN user is logged in (POST)
    THEN check the response is valid
    """
    login_response = login_user(test_client)
    assert login_response.status_code == 200

    """
    WHEN the logged in user requests('/home') (GET)
    THEN check the response is valid
    """
    response = test_client.get('/home', follow_redirects=True)
    assert response.status_code == 200
    assert b"View and edit" in response.data
