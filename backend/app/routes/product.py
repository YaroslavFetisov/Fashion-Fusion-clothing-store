import os
import uuid

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..models import Product, Category, ProductImage
from ..utils.db import db
from ..utils.decorators import admin_required

bp = Blueprint('product', __name__, url_prefix='/product')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/add', methods=['POST'])
@admin_required
def add_product():
    try:
        data = request.form
        required_fields = ['name', 'price', 'category_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'{field.capitalize()} is required'}), 400

        stock_quantity = int(data.get('stock_quantity', 0))
        if stock_quantity < 0:
            return jsonify({'message': 'Stock quantity cannot be negative.'}), 400

        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'message': 'Category does not exist'}), 404

        # Отримання списку файлів з запиту
        files = request.files.getlist('files')

        # Перевірка чи були відправлені файли
        if 'files' not in request.files or len(files) == 0:
            return jsonify({'error': 'No files part or no files selected'}), 400

        # Ініціалізація списку для зберігання унікальних імен файлів
        image_paths = []

        # Збереження кожного файлу на сервері з унікальним ім'ям
        for file in files:
            if file.filename == '':
                continue
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Генерація унікального імені для файлу
                unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                image_paths.append(unique_filename)
            else:
                return jsonify({'error': 'File type not allowed'}), 400

        # Створення нового продукту з зображеннями
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            stock_quantity=stock_quantity,
            category_id=int(data['category_id']),
            size=data.get('size', ''),
            color=data.get('color', ''),
            gender=data.get('gender', '')
        )

        # Збереження нового продукту в базі даних
        db.session.add(new_product)
        db.session.commit()

        # Збереження шляхів до зображень продукту в таблиці ProductImage
        for image_path in image_paths:
            product_image = ProductImage(product_id=new_product.id, image_filename=image_path)
            db.session.add(product_image)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@bp.route('/update/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    try:
        data = request.form
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        stock_quantity = int(data.get('stock_quantity', product.stock_quantity))
        if stock_quantity < 0:
            return jsonify({'message': 'Stock quantity cannot be negative.'}), 400

        # Перевірка існування категорії
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'message': 'Category does not exist'}), 404

        # Отримання списку файлів з запиту
        files = request.files.getlist('files')

        # Перевірка чи були відправлені нові файли
        if 'files' in request.files and len(files) > 0:
            # Ініціалізація списку для зберігання унікальних імен файлів
            new_image_paths = []

            # Збереження нових файлів на сервері з унікальним іменем
            for file in files:
                if file.filename == '':
                    continue
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Генерація унікального імені для файлу
                    unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(file_path)
                    new_image_paths.append(unique_filename)
                else:
                    return jsonify({'error': 'File type not allowed'}), 400

            # Видалення старих зображень продукту з файлової системи і бази даних
            old_images = ProductImage.query.filter_by(product_id=product.id).all()
            for old_image in old_images:
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_image.image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
                db.session.delete(old_image)

            # Збереження шляхів до нових зображень продукту в таблиці ProductImage
            for new_image_path in new_image_paths:
                product_image = ProductImage(product_id=product.id, image_filename=new_image_path)
                db.session.add(product_image)

        # Оновлення полів продукту
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.stock_quantity = stock_quantity
        product.category_id = int(data.get('category_id', product.category_id))
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

        # Видалення зображень продукту з файлової системи
        product_images = ProductImage.query.filter_by(product_id=product.id).all()
        for product_image in product_images:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product_image.image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)

        # Видалення зображень продукту з бази даних
        ProductImage.query.filter_by(product_id=product.id).delete()

        # Видалення продукту з бази даних
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
                'gender': product.gender,
                'images': []
            }

            images = ProductImage.query.filter_by(product_id=product.id).all()
            for image in images:
                product_info['images'].append(image.image_filename)

            product_list.append(product_info)

        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500
