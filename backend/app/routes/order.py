from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime
from pytz import timezone
from ..models import Order, OrderItem, CartItem
from ..utils.db import db
from ..utils.decorators import customer_required, admin_required

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/create', methods=['POST'])
@customer_required
def create_order():
    try:
        cart_items = CartItem.query.filter_by(cart_id=current_user.cart.id).all()
        if not cart_items:
            return jsonify({"error": "Cart is empty. Add items to cart first."}), 400

        # Check product availability and update stock
        for item in cart_items:
            if item.product.stock_quantity - item.quantity < 0:
                return jsonify({"error": "Insufficient stock for product '{}'".format(item.product.name)}), 400
            item.product.stock_quantity -= item.quantity

        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        order = Order(
            status="Pending",
            total_amount=total_amount,
            created_at=datetime.now(timezone('Europe/Kiev')).astimezone(timezone('UTC+3')),  # Час створення, з поясом +3
            updated_at=datetime.now(timezone('Europe/Kiev')).astimezone(timezone('UTC+3')),  # Час оновлення, з поясом +3
            customer=current_user,
            items=[]
        )

        for cart_item in cart_items:
            order_item = OrderItem(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                size=cart_item.product.size,
                category=cart_item.product.category.name
            )
            order.items.append(order_item)

        db.session.add(order)

        current_user.cart.items.clear()

        db.session.commit()

        return jsonify({"message": "Order created successfully.", "order_id": order.id}), 201

    except Exception as e:
        db.session.rollback()  # Rollback on error
        error_message = "Error occurred while creating order: {}".format(str(e))
        return jsonify({"error": error_message}), 500


@bp.route('/update_status/<int:order_id>', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found."}), 404

        data = request.get_json()
        new_status = data.get('status')

        if not new_status:
            return jsonify({"error": "New status is required."}), 400

        order.status = new_status
        db.session.commit()

        return jsonify({"message": "Order status updated successfully."}), 200

    except Exception as e:
        error_message = "Error occurred while updating order status: {}".format(str(e))
        return jsonify({"error": error_message}), 500


@bp.route('/list', methods=['GET'])
@admin_required
def list_orders():
    try:
        orders = Order.query.all()
        if not orders:
            return jsonify({"message": "No orders found."}), 404

        order_list = []
        for order in orders:
            order_info = {
                'order_id': order.id,
                'status': order.status,
                'total_amount': order.total_amount,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat(),
                'customer': {
                    'id': order.customer.id,
                    'name': order.customer.name,
                    'email': order.customer.email,
                    'address': order.customer.address
                },
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
                    'gender': item.product.gender,
                    'size': item.product.size
                }
                order_info['order_items'].append(product_info)
            order_list.append(order_info)

        return jsonify(order_list), 200

    except Exception as e:
        error_message = "Error occurred while retrieving orders: {}".format(str(e))
        return jsonify({"error": error_message}), 500
