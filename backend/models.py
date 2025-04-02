from backend.extensions import mongo, login_manager
from flask_login import UserMixin
from bson.objectid import ObjectId  # ✅ Import ObjectId

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})  # ✅ Convert ID to ObjectId
        if user_data:
            return User(user_data)  # ✅ Return a User object
    except Exception as e:
        print(f"Error loading user: {e}")  # Debugging
    return None

# User Model (MongoDB)
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])  # ✅ Convert ObjectId to string
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.password = user_data["password"]

    def get_id(self):
        return self.id  # ✅ Ensure Flask-Login gets a string ID
