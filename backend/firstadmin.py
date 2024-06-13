from app import create_app
from app.models import Admin
from app.utils.db import db
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin = Admin(
        id=666,
        name='Admin',
        email='admin@gmail.com',
        password=generate_password_hash('admin'),
        address='Admin Address'
    )
    db.session.add(admin)
    db.session.commit()

print('Admin created successfully!')
