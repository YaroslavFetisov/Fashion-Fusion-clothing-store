from flask.testing import FlaskClient
from backend.app.models import Customer, Product, Category
from backend.app.utils.db import db
from backend.app.models import Order, OrderItem, ProductImage
from datetime import datetime


def register_customer(client: FlaskClient, name: str, email: str, password: str, address: str):
    return client.post('/customer/register', json={
        'name': name,
        'email': email,
        'password': password,
        'address': address
    })


def login_customer(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


def test_register_customer(client: FlaskClient):
    response = register_customer(client, 'Test User', 'testuser@example.com', 'password', '123 Test St')
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Customer registered successfully'


def test_register_existing_email(client: FlaskClient, customer_user: Customer):
    response = register_customer(client, 'Another User', customer_user.email, 'password', '123 Test St')
    print("Res:", response.get_json())
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Email address is already registered'


def test_register_missing_field(client: FlaskClient):
    response = client.post('/customer/register', json={'name': 'Test User', 'email': 'testuser@example.com'})
    assert response.status_code == 400
    assert 'message' in response.get_json()


def test_customer_profile(client: FlaskClient, customer_user: Customer):
    client = login_customer(client, customer_user.email, 'customer')
    response = client.get('/customer/profile')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == customer_user.name
    assert data['email'] == customer_user.email
    assert data['address'] == customer_user.address


def test_customer_profile_orders(client: FlaskClient, customer_user: Customer):
    client = login_customer(client, customer_user.email, 'customer')

    with client.application.app_context():
        category = Category(name="Test Category")
        db.session.add(category)
        db.session.commit()

        product = Product(name='Test Product', description='Test Description', price=10.0, stock_quantity=5,
                          category_id=category.id, size='M', color='Blue', gender='Unisex')
        db.session.add(product)
        db.session.commit()

        image = ProductImage(product_id=product.id, image_filename='test_image.jpg')
        db.session.add(image)
        db.session.commit()

        order = Order(customer_id=customer_user.id, created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total_amount=20.0)
        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(order_id=order.id, product_id=product.id, price=10.0, quantity=2)
        db.session.add(order_item)
        db.session.commit()

    response = client.get('/customer/profile')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['orders']) == 1
    assert data['orders'][0]['order_items'][0]['name'] == 'Test Product'
    assert data['orders'][0]['order_items'][0]['images'] == ['test_image.jpg']
