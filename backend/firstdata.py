from app import create_app
from app.models import Category, Product, Customer, Cart, CartItem
from app.utils.db import db
from werkzeug.security import generate_password_hash
from flask_login import login_user

app = create_app()

with app.app_context():
    # Створення нової категорії "Одяг"
    category_clothing = Category(
        name='Category'
    )
    db.session.add(category_clothing)
    db.session.commit()

    print('Category created successfully!')

    # Створення нового товару - футболка
    product_tshirt = Product(
        name='T-shirt',
        description='Casual cotton t-shirt',
        price=19.99,
        stock_quantity=100,
        category_id=category_clothing.id,
        size='Large',
        color='White',
        gender='Unisex'
    )
    db.session.add(product_tshirt)
    db.session.commit()

    print('T-shirt created successfully!')

    # Реєстрація нового покупця
    customer = Customer(
        name='Customer',
        email='customer@gmail.com',
        password=generate_password_hash('customer'),
        address='1234 Customer Street'
    )
    db.session.add(customer)
    db.session.commit()

    print('Customer registered successfully!')

    # Створення кошика для покупця
    cart = Cart(
        customer_id=customer.id
    )
    db.session.add(cart)
    db.session.commit()

    print('Cart created successfully!')

    # Додавання товару до кошика покупця
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=product_tshirt.id,
        quantity=2
    )
    db.session.add(cart_item)
    db.session.commit()

    print('CartItem created successfully!')

print('Data initialization completed!')