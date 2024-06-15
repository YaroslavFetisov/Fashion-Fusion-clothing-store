from flask.testing import FlaskClient
from backend.app.models import Admin


def login_as_admin(client: FlaskClient, admin_user: Admin):
    response = client.post('/auth/login', json={'email': admin_user.email, 'password': 'admin'})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


def test_profile(client: FlaskClient, admin_user: Admin):
    client = login_as_admin(client, admin_user)
    response = client.get('/admin/profile')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == admin_user.name
    assert data['email'] == admin_user.email
    assert data['address'] == admin_user.address


def test_update_profile(client: FlaskClient, admin_user: Admin):
    client = login_as_admin(client, admin_user)
    update_data = {'name': 'Updated Name', 'address': '456 Updated St'}
    response = client.put('/admin/update_profile', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Profile updated successfully'

    updated_admin = Admin.query.get(admin_user.id)
    assert updated_admin.name == 'Updated Name'
    assert updated_admin.address == '456 Updated St'

def test_create_admin(client: FlaskClient, admin_user: Admin):
    client = login_as_admin(client, admin_user)
    new_admin_data = {
        'name': 'New Admin',
        'email': 'newadmin@example.com',
        'password': 'newadminpassword',
        'address': '789 New St'
    }
    response = client.post('/admin/create_admin', json=new_admin_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Admin created successfully'

    new_admin = Admin.query.filter_by(email='newadmin@example.com').first()
    assert new_admin is not None
    assert new_admin.name == 'New Admin'
    assert new_admin.address == '789 New St'

def test_get_all_admins(client: FlaskClient, admin_user: Admin):
    client = login_as_admin(client, admin_user)
    response = client.get('/admin/get_all_admins')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['email'] == admin_user.email

def test_search_admin(client: FlaskClient, admin_user: Admin):
    client = login_as_admin(client, admin_user)
    response = client.get(f'/admin/search_admin/{admin_user.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == admin_user.email

    response = client.get('/admin/search_admin/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Admin not found'
