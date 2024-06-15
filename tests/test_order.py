from flask import Flask
from flask.testing import FlaskClient
from backend.app.models import Admin, Customer, Order, Product


def login_as_customer(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


def login_as_admin(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


def test_create_order(client: FlaskClient, app: Flask, customer_user: Customer, sample_product: Product):
    client = login_as_customer(client, customer_user.email, 'customer')

    response = client.post('/cart/add', json={'product_id': sample_product.id, 'quantity': 1})
    print(response.get_json())
    assert response.status_code == 200

    response = client.post('/order/create')
    assert response.status_code == 201
    print(response.get_json())
    assert 'order_id' in response.json
    assert response.json['message'] == 'Order created successfully.'


def test_update_order_status(client: FlaskClient, app: Flask, admin_user: Admin, sample_order: Order):
    client = login_as_admin(client, admin_user.email, 'admin')

    order_id = sample_order.id
    new_status = 'Shipped'

    response = client.put(f'/order/update_status/{order_id}', json={'status': new_status})
    assert response.status_code == 200
    assert response.json['message'] == 'Order status updated successfully.'


def test_list_orders(client: FlaskClient, app: Flask, admin_user: Admin, sample_order: Order):
    client = login_as_admin(client, admin_user.email, 'admin')

    response = client.get('/order/list')
    assert response.status_code == 200
    assert len(response.json) == 1

    order_info = response.json[0]
    assert 'order_id' in order_info
    assert 'status' in order_info
    assert 'total_amount' in order_info
    assert 'created_at' in order_info
    assert 'updated_at' in order_info
    assert 'customer' in order_info
    assert 'order_items' in order_info
    assert len(order_info['order_items']) == 1

    product_info = order_info['order_items'][0]
    assert 'product_id' in product_info
    assert 'name' in product_info
    assert 'description' in product_info
    assert 'price' in product_info
    assert 'quantity' in product_info
    assert 'total_price' in product_info
    assert 'gender' in product_info
    assert 'size' in product_info
    assert 'images' in product_info