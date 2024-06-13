from flask import Blueprint, request, jsonify
from ..models import Product, Category
from ..utils.db import db
from ..utils.decorators import admin_required

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/add', methods=['POST'])
@admin_required
def add_product():
    try:
        data = request.get_json()
        required_fields = ['name', 'price', 'category_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'{field.capitalize()} is required'}), 400

        stock_quantity = data.get('stock_quantity', 0)
        if stock_quantity < 0:
            return jsonify({'message': 'Stock quantity cannot be negative.'}), 400

        # Перевірка існування категорії
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'message': 'Category does not exist'}), 404

        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock_quantity=stock_quantity,
            category_id=data['category_id'],
            size=data.get('size', ''),
            color=data.get('color', ''),
            gender=data.get('gender', '')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500



@bp.route('/update/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    try:
        data = request.get_json()
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        stock_quantity = data.get('stock_quantity', product.stock_quantity)
        if stock_quantity < 0:
            return jsonify({'message': 'Stock quantity cannot be negative.'}), 400

        # Перевірка існування категорії
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'message': 'Category does not exist'}), 404

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.stock_quantity = stock_quantity
        product.category_id = data.get('category_id', product.category_id)
        product.size = data.get('size', product.size)
        product.color = data.get('color', product.color)
        product.gender = data.get('gender', product.gender)

        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@bp.route('/delete/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@bp.route('/list', methods=['GET'])
def list_products():
    try:
        products = Product.query.all()
        if not products:
            return jsonify({'message': 'No products found'}), 404

        product_list = []
        for product in products:
            product_info = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock_quantity': product.stock_quantity,
                'category_id': product.category_id,
                'size': product.size,
                'color': product.color,
                'gender': product.gender
            }
            product_list.append(product_info)

        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500
