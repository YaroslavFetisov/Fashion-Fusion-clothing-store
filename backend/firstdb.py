from app import create_app
from app.utils.db import db

app = create_app()
app.app_context().push()
db.create_all()
exit()
