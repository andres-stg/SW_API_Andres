# src/admin.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, People, Planet, Favorite

def setup_admin(app):
    admin = Admin(app, name='Star Wars API', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Favorite, db.session))

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))