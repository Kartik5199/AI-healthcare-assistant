
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect  # ✅ Add CSRF protection


mongo = PyMongo()
bcrypt = Bcrypt()
csrf = CSRFProtect()  # ✅ Initialize CSRF
login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info'
