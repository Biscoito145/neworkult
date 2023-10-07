from neworkut import app, database
from neworkut.models import Usuario, Post

with app.app_context():
    database.create_all()