from flask import Blueprint, request, jsonify
from flask_login import current_user
from ..models import Cart, Product, CartItem, ProductImage
from ..utils.db import db
from ..utils.decorators import customer_required

bp = Blueprint('cart', __name__, url_prefix='/cart')


@bp.route('/add', methods=['POST'])
@customer_required
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity:
            return jsonify({"error": "Product ID and quantity are required."}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found."}), 404

        if product.stock_quantity < quantity:
            return jsonify({"error": "Insufficient stock quantity."}), 400

        cart = current_user.cart
        if not cart:
            cart = Cart(customer_id=current_user.id)
            db.session.add(cart)

        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()

        return jsonify({"message": "Product added to cart successfully."}), 200

    except Exception as e:
        error_message = "Error occurred while adding product to cart: {}".format(str(e))
        return jsonify({"error": error_message}), 500


@bp.route('/update', methods=['PUT'])
@customer_required
def update_cart():
    try:
        data = request.get_json()
        updates = data.get('updates')

        if not updates:
            return jsonify({"error": "No updates provided."}), 400

        for update in updates:
            product_id = update.get('product_id')
            quantity = update.get('quantity')

            if not product_id or not quantity:
                return jsonify({"error": "Product ID and quantity are required for each update."}), 400

            cart_item = CartItem.query.filter_by(cart_id=current_user.cart.id, product_id=product_id).first()
            if not cart_item:
                return jsonify({"error": f"Product with ID {product_id} not found in cart."}), 404

            if quantity <= 0:
                db.session.delete(cart_item)
            else:
                product = Product.query.get(product_id)
                if not product:
                    return jsonify({"error": f"Product with ID {product_id} not found."}), 404

                if product.stock_quantity < quantity:
                    return jsonify({"error": "Insufficient stock quantity for product with ID {}.".format(product_id)}), 400

                cart_item.quantity = quantity

        db.session.commit()

        return jsonify({"message": "Cart updated successfully."}), 200

    except Exception as e:
        error_message = "Error occurred while updating cart: {}".format(str(e))
        return jsonify({"error": error_message}), 500


@bp.route('/view', methods=['GET'])
@customer_required
def view_cart():
    try:
        cart_items = CartItem.query.filter_by(cart_id=current_user.cart.id).all()
        cart_info = []
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            if not product:
                return jsonify({"error": f"Product with ID {cart_item.product_id} not found"}), 404

            product_info = {
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": cart_item.quantity,
                "total_price": product.price * cart_item.quantity,
                "size": product.size,
                "color": product.color,
                "gender": product.gender,
                "category": product.category.name,
                "images": []
            }

            # Отримання фотографій продукту
            images = ProductImage.query.filter_by(product_id=product.id).all()
            for image in images:
                product_info['images'].append(image.image_filename)

            cart_info.append(product_info)

        return jsonify(cart_info), 200

    except Exception as e:
        error_message = "Error occurred while viewing cart: {}".format(str(e))
        return jsonify({"error": error_message}), 500


@bp.route('/clear', methods=['DELETE'])
@customer_required
def clear_cart():
    try:
        CartItem.query.filter_by(cart_id=current_user.cart.id).delete()
        db.session.commit()

        return jsonify({"message": "Cart cleared successfully."}), 200

    except Exception as e:
        error_message = "Error occurred while clearing cart: {}".format(str(e))
        return jsonify({"error": error_message}), 500
