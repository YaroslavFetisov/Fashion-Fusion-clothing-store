from flask import Flask, jsonify
from flask.testing import FlaskClient
from backend.app.models import Customer, Product

def login_as_customer(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client

def test_add_to_cart(client: FlaskClient, app: Flask, customer_user: Customer, product: Product):
    client = login_as_customer(client, customer_user.email, 'customer')

    data = {'product_id': product.id, 'quantity': 2}
    response = client.post('/cart/add', json=data)
    assert response.status_code == 200
    assert response.json['message'] == 'Product added to cart successfully.'

    data['quantity'] = 20
    response = client.post('/cart/add', json=data)
    assert response.status_code == 400
    assert response.json['error'] == 'Insufficient stock quantity.'

def test_update_cart(client: FlaskClient, app: Flask, customer_user: Customer, product: Product):
    client = login_as_customer(client, customer_user.email, 'customer')

    data = {'product_id': product.id, 'quantity': 2}
    client.post('/cart/add', json=data)

    update_data = {'updates': [{'product_id': product.id, 'quantity': 5}]}
    response = client.put('/cart/update', json=update_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Cart updated successfully.'

    invalid_update_data = {'updates': [{'product_id': 999, 'quantity': 5}]}
    response = client.put('/cart/update', json=invalid_update_data)
    assert response.status_code == 404
    assert response.json['error'] == 'Product with ID 999 not found in cart.'

def test_view_cart(client: FlaskClient, app: Flask, customer_user: Customer, product: Product):
    client = login_as_customer(client, customer_user.email, 'customer')

    data = {'product_id': product.id, 'quantity': 2}
    client.post('/cart/add', json=data)
    response = client.get('/cart/view')
    assert response.status_code == 200
    assert len(response.json) == 1

    cart_item = response.json[0]
    assert cart_item['product_id'] == product.id
    assert cart_item['name'] == product.name
    assert cart_item['description'] == product.description
    assert cart_item['price'] == product.price
    assert cart_item['quantity'] == 2

def test_clear_cart(client: FlaskClient, app: Flask, customer_user: Customer, product: Product):
    client = login_as_customer(client, customer_user.email, 'customer')

    data = {'product_id': product.id, 'quantity': 2}
    client.post('/cart/add', json=data)

    response = client.delete('/cart/clear')
    assert response.status_code == 200
    assert response.json['message'] == 'Cart cleared successfully.'
    response = client.get('/cart/view')
    assert response.status_code == 200