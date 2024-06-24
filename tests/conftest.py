import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash
from backend.app import create_app
from backend.app.utils.db import db
from backend.app.models import Admin, Customer, Order, OrderItem, Cart, CartItem, Product, ProductImage, Category
from tempfile import TemporaryDirectory
from datetime import datetime

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['UPLOAD_FOLDER'] = '/temp'  # Temporary folder for testing uploads
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def admin_user(app: Flask):
    admin = Admin(
        id=666,
        name='Admin User',
        email='admin@gmail.com',
        password=generate_password_hash('admin'),
        address='123 Admin St'
    )
    with app.app_context():
        db.session.add(admin)
        db.session.commit()
        yield admin
        db.session.delete(admin)
        db.session.commit()

@pytest.fixture
def customer_user(app: Flask):
    customer = Customer(
        id=1,
        name='Customer User',
        email='customer@gmail.com',
        password=generate_password_hash('customer'),
        address='123 Customer St'
    )
    with app.app_context():
        db.session.add(customer)
        db.session.commit()
        db.session.refresh(customer)  # Refresh to bind to session
        yield customer
        db.session.delete(customer)
        db.session.commit()

def login_customer(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


@pytest.fixture
def category():
    category = Category(name='Test Category')
    db.session.add(category)
    db.session.commit()
    return category

@pytest.fixture
def upload_folder(app):
    with TemporaryDirectory() as tempdir:
        app.config['UPLOAD_FOLDER'] = tempdir
        yield tempdir

@pytest.fixture
def sample_product(app: Flask, category: Category):
    product = Product(
        name='Test Product',
        description='Test Description',
        price=10.0,
        stock_quantity=10,
        category_id=category.id,
        size='M',
        color='Blue',
        gender='Unisex'
    )
    with app.app_context():
        db.session.add(product)
        db.session.commit()
        yield product
        db.session.delete(product)
        db.session.commit()

@pytest.fixture
def sample_order(app: Flask, customer_user: Customer, sample_product: Product):
    order = Order(
        status='Pending',
        total_amount=10.0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        customer=customer_user,
    )
    order_item = OrderItem(
        product=sample_product,
        quantity=1,
        price=10.0
    )
    order.items.append(order_item)
    with app.app_context():
        db.session.add(order)
        db.session.commit()
        yield order
        db.session.delete(order)
        db.session.commit()

@pytest.fixture
def product(app: Flask):
    category = Category(name='Test Category')
    product = Product(
        name='Test Product',
        description='Test Description',
        price=10.0,
        stock_quantity=10,
        category=category
    )
    with app.app_context():
        db.session.add(category)
        db.session.add(product)
        db.session.commit()
        yield product
        db.session.delete(product)
        db.session.delete(category)
        db.session.commit()