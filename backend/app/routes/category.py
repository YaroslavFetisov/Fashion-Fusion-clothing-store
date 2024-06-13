from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from ..models import Category
from ..utils.db import db
from ..utils.decorators import admin_required

bp = Blueprint('category', __name__, url_prefix='/category')


@bp.route('/add', methods=['POST'])
@admin_required
def add_category():
    data = request.get_json()
    try:
        if 'name' not in data or not data['name']:
            return jsonify({'message': 'Category name is required'}), 400

        new_category = Category(
            name=data['name']
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category added successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        error_info = str(e.orig)
        if 'UNIQUE constraint failed: category.name' in error_info:
            return jsonify({'message': 'Category with this name already exists'}), 400
        else:
            return jsonify({'message': 'Error: {}'.format(error_info)}), 500
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@bp.route('/delete/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@bp.route('/list', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    if not categories:
        return jsonify({'message': 'No categories found'}), 404

    return jsonify([{
        'id': category.id,
        'name': category.name
    } for category in categories]), 200
