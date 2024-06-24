from flask import Flask
from flask.testing import FlaskClient
from backend.app.models import Admin, Category


def login_as_admin(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


def test_add_category(client: FlaskClient, app: Flask, admin_user: Admin):
    client = login_as_admin(client, admin_user.email, 'admin')

    category_data = {'name': 'New Category'}
    response = client.post('/category/add', json=category_data)
    assert response.status_code == 201
    assert response.json['message'] == 'Category added successfully'

    response = client.post('/category/add', json=category_data)
    assert response.status_code == 400
    assert response.json['message'] == 'Category with this name already exists'

    response = client.post('/category/add', json={})
    assert response.status_code == 400
    assert response.json['message'] == 'Category name is required'


def test_delete_category(client: FlaskClient, app: Flask, admin_user: Admin, category: Category):
    client = login_as_admin(client, admin_user.email, 'admin')

    response = client.delete(f'/category/delete/{category.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Category deleted successfully'

    response = client.delete('/category/delete/999')
    assert response.status_code == 404
    assert response.json['message'] == 'Category not found'


def test_list_categories(client: FlaskClient, app: Flask, category: Category):
    response = client.get('/category/list')
    assert response.status_code == 200
    assert len(response.json) == 1

    category_info = response.json[0]
    assert 'id' in category_info
    assert 'name' in category_info