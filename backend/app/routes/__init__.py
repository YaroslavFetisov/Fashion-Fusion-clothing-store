from flask import Blueprint

bp = Blueprint('routes', __name__)

from . import auth, customer, admin, order, product, category