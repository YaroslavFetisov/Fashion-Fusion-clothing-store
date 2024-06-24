from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from ..models import Customer, Admin
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Customer.query.filter_by(email=email).first() or Admin.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    login_user(user)
    return jsonify({'message': 'Login successful'}), 200


@bp.route('/logout', methods=['POST'])
@login_required
def logout_route():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200
