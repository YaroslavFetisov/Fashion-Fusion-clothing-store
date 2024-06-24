from flask.testing import FlaskClient
from backend.app.models import Admin

def login_as_admin(client: FlaskClient, admin_user: Admin):
    response = client.post('/auth/login', json={'email': admin_user.email, 'password': 'admin'})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client

def test_login_success(client: FlaskClient, admin_user: Admin):
    response = client.post('/auth/login', json={'email': admin_user.email, 'password': 'admin'})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'

def test_login_failure(client: FlaskClient):
    response = client.post('/auth/login', json={'email': 'wrong@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid email or password'

def test_logout(client: FlaskClient, admin_user: Admin):
    client = login_as_admin(client, admin_user)
    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Logout successful'