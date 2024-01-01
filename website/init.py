from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__,template_folder='template',static_folder='static')
    app.config['SECRET_KEY'] = 'replace_this_with_a_more_secure_key76.2*39'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views


    app.register_blueprint(views)


    from .models import User
    
    create_database(app)
    create_admin_user(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

def create_admin_user(app):
    with app.app_context():
        from .models import User
        """Hardcodes a user with an admin role into the database."""
        admin_email = "admin@example.com"
        admin_password = "123456789"  # This should be properly hashed in a real scenario
        admin_name = "Admin User"

        # Check if admin user already exists
        admin_user = User.query.filter_by(email=admin_email).first()
        if admin_user:
            print("Admin user already exists.")
        else:
            # Create and insert the new admin user
            new_admin = User(email=admin_email, password=generate_password_hash(admin_password), name=admin_name, role="admin")
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created.")
