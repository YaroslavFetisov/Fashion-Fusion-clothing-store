from flask import Flask
from .utils.db import db
from flask_login import LoginManager
from .models import Customer, Admin
from .routes import auth, customer, admin, order, product, category, cart
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object('config.Config')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id)) or Customer.query.get(int(user_id))

    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(cart.bp)

    return app
