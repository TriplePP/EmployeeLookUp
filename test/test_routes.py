from test.conftest import test_client


def test_register(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200


def test_login(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200


def test_home(test_client, init_database):
    response = test_client.get('/')
    assert response.status_code == 200
