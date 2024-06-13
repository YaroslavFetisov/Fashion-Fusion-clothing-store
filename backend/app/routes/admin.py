from flask import Blueprint, request, jsonify
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from ..models import Admin
from ..utils.db import db
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash
import time

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/profile', methods=['GET'])
@admin_required
def profile():
    admin = Admin.query.get(current_user.id)
    if not admin:
        return jsonify(message="Admin not found"), 404
    return jsonify({
        'name': admin.name,
        'email': admin.email,
        'address': admin.address
    }), 200


@bp.route('/update_profile', methods=['PUT'])
@admin_required
def update_profile():
    data = request.get_json()
    admin = Admin.query.get(current_user.id)
    if not admin:
        return jsonify(message="Admin not found"), 404

    admin.name = data.get('name', admin.name)
    admin.email = data.get('email', admin.email)
    admin.address = data.get('address', admin.address)

    if 'password' in data:
        admin.password = generate_password_hash(data['password'])

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Admin with this email already exists"), 400
    except Exception as e:
        return jsonify(message="Error: {}".format(str(e))), 500


@bp.route('/create_admin', methods=['POST'])
@admin_required
def create_admin():
    data = request.get_json()
    try:
        new_admin = Admin(
            id=int(time.time()),
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            address=data.get('address')
        )
        db.session.add(new_admin)
        db.session.commit()
        return jsonify(message="Admin created successfully"), 201
    except KeyError as e:
        missing_field = str(e).strip("'")
        return jsonify(message=f"Missing required field: {missing_field}"), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Admin with this email already exists"), 400
    except Exception as e:
        return jsonify(message="Error: {}".format(str(e))), 500


@bp.route('/get_all_admins', methods=['GET'])
def get_all_admins():
    admins = Admin.query.all()
    admin_list = []
    for admin in admins:
        admin_list.append({
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'address': admin.address,
        })
    return jsonify(admin_list), 200


@bp.route('/search_admin/<int:id>', methods=['GET'])
@admin_required
def search_admin(id):
    admin = Admin.query.get(id)
    if admin:
        admin_data = {
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'address': admin.address
        }
        return jsonify(admin_data), 200
    else:
        return jsonify(message="Admin not found"), 404
