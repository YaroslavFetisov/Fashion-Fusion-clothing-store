from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user
from werkzeug.security import generate_password_hash
from ..models import Customer, Order
from ..utils.db import db
from ..utils.decorators import customer_required

bp = Blueprint('customer', __name__, url_prefix='/customer')


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        required_fields = ['name', 'email', 'password', 'address']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'{field.capitalize()} is required'}), 400

        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            address=data['address']
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer registered successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        error_info = str(e.orig)
        if 'UNIQUE constraint failed: customer.email' in error_info:
            return jsonify({'message': 'Email address is already registered'}), 400
        else:
            return jsonify({'message': 'Error: {}'.format(error_info)}), 500
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@bp.route('/profile', methods=['GET'])
@customer_required
def profile():
    try:
        customer = Customer.query.get(current_user.id)
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404

        orders = Order.query.filter_by(customer_id=current_user.id).all()
        order_list = []
        for order in orders:
            order_info = {
                'order_id': order.id,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'status': order.status,
                'total_amount': order.total_amount,
                'order_items': []
            }
            for item in order.items:
                product_info = {
                    'product_id': item.product.id,
                    'name': item.product.name,
                    'description': item.product.description,
                    'price': item.price,
                    'quantity': item.quantity,
                    'total_price': item.price * item.quantity,
                    'category': item.product.category.name,
                    'size': item.product.size,
                    'color': item.product.color,
                    'gender': item.product.gender
                }
                order_info['order_items'].append(product_info)
            order_list.append(order_info)

        profile_info = {
            'name': customer.name,
            'email': customer.email,
            'address': customer.address,
            'orders': order_list
        }
        return jsonify(profile_info), 200
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


