import os
import io
from flask import Flask
from flask.testing import FlaskClient
from backend.app.models import Product, Category, ProductImage
from backend.app.utils.db import db
from backend.app.models import Admin

def login_customer(client: FlaskClient, email: str, password: str):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client

def login_as_admin(client: FlaskClient, admin_user: Admin):
    response = client.post('/auth/login', json={'email': admin_user.email, 'password': 'admin'})
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    return client


def test_add_product_with_image(client: FlaskClient, app: Flask, admin_user: Admin, category: Category, upload_folder: str):
    client = login_as_admin(client, admin_user)
    data = {
        'name': 'Test Product',
        'description': 'Test Description',
        'price': '10.0',
        'stock_quantity': '5',
        'category_id': category.id,
        'size': 'M',
        'color': 'Blue',
        'gender': 'Unisex'
    }
    image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

    with open(image_path, 'rb') as img_file:
        data['files'] = (img_file, 'test_image.jpg')

        response = client.post('/product/add', data=data, content_type='multipart/form-data')

        assert response.status_code == 201
        assert response.json['message'] == 'Product added successfully'

        with app.app_context():
            product = Product.query.filter_by(name='Test Product').first()
            assert product is not None
            assert product.name == 'Test Product'
            assert product.description == 'Test Description'
            assert product.price == 10.0
            assert product.stock_quantity == 5
            assert product.category_id == category.id

            product_images = ProductImage.query.filter_by(product_id=product.id).all()
            assert len(product_images) == 1


def test_update_product(client: FlaskClient, admin_user: Admin, category: Category):
    client = login_as_admin(client, admin_user)

    product = Product(name='Test Product', description='Test Description', price=10.0, stock_quantity=5,
                      category_id=category.id, size='M', color='Blue', gender='Unisex')
    db.session.add(product)
    db.session.commit()

    data = {
        'name': 'Updated Product',
        'description': 'Updated Description',
        'price': '15.0',
        'stock_quantity': '10',
        'category_id': str(category.id),
        'size': 'L',
        'color': 'Red',
        'gender': 'Female'
    }
    data_file = {'files': (io.BytesIO(b"file_content"), 'updated_image.jpg')}

    response = client.put(f'/product/update/{product.id}', data={**data, 'files': data_file},
                          content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product updated successfully'


def test_delete_product(client: FlaskClient, admin_user: Admin, category: Category):
    client = login_as_admin(client, admin_user)

    product = Product(name='Test Product', description='Test Description', price=10.0, stock_quantity=5,
                      category_id=category.id, size='M', color='Blue', gender='Unisex')
    db.session.add(product)
    db.session.commit()

    response = client.delete(f'/product/delete/{product.id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product deleted successfully'


def test_list_products(client: FlaskClient, admin_user: Admin, category: Category):
    client = login_as_admin(client, admin_user)

    product = Product(name='Test Product', description='Test Description', price=10.0, stock_quantity=5,
                      category_id=category.id, size='M', color='Blue', gender='Unisex')
    db.session.add(product)
    db.session.commit()

    image = ProductImage(product_id=product.id, image_filename='test_image.jpg')
    db.session.add(image)
    db.session.commit()

    response = client.get('/product/list')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert data[0]['name'] == 'Test Product'
    assert data[0]['images'] == ['test_image.jpg']