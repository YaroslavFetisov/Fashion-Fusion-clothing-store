from flask import abort
from flask_login import current_user
from functools import wraps
from ..models import Admin, Customer


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Customer):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
