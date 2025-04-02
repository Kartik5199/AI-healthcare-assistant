from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
import re
from backend.extensions import bcrypt, mongo
from backend.models import User
from backend.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from backend.predict import predict_disease, predict_brain_tumor  
from pymongo.errors import DuplicateKeyError
from .chatbot import get_chatbot_response  
from . import csrf
routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def home():
    return render_template("index.html")

@routes_bp.route("/register", methods=["GET", "POST"])
def register():
    print("Register route triggered!")  

    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard"))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        print("Form validated!")  

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        user_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password
        }

        if mongo.db.users.find_one({"username": form.username.data}):
            flash("Username already exists. Choose another.", "danger")
            return redirect(url_for("routes.register"))

        if mongo.db.users.find_one({"email": form.email.data}):
            flash("Email already registered. Use a different one.", "danger")
            return redirect(url_for("routes.register"))

        try:
            result = mongo.db.users.insert_one(user_data)  
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("routes.login"))

        except DuplicateKeyError:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("routes.register"))

    print("Form errors:", form.errors)
    return render_template("register.html", form=form)

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data})  

        if user and bcrypt.check_password_hash(user["password"], form.password.data):
            user_obj = User(user)
            login_user(user_obj) 

            flash('Login successful!', 'success')
            next_page = request.args.get("next")  
            return redirect(next_page) if next_page else redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

@routes_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.home"))

@routes_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

@routes_bp.route("/predict_disease", methods=["GET", "POST"])
@login_required
def disease_prediction():
    symptoms = request.form.getlist("symptoms")
    prediction = predict_disease(symptoms)  
    return render_template("disease_prediction.html", prediction=prediction)

@routes_bp.route("/brain_tumor", methods=["GET", "POST"])
@login_required
def brain_tumor():
    return render_template("brain_tumor.html")

@routes_bp.route('/medicine', methods=["GET", "POST"])
@csrf.exempt
@login_required
def get_medicine():
    medicine_name = request.form.get("medicine_name", "").strip()
    disease_name = request.form.get("disease_name", "").strip()

    print(f" Received medicine_name: '{medicine_name}'")
    print(f" Received disease_name: '{disease_name}'")

    medicines = []

    if disease_name:
        #  Fetch only medicine names, no medicine details
        disease_entry = mongo.db.drug_disease.find_one(
            {"disease": {"$regex": f"^{disease_name}$", "$options": "i"}},  
            {"_id": 0}
        )
        print(f" Disease search result: {disease_entry}")

        if disease_entry:
            medicines = disease_entry.get("medicines", [])  
            print(f" Medicines found for {disease_name}: {medicines}")

    elif medicine_name:
        #  Fetch full medicine details by name
        medicine_data = mongo.db.medicine_details.find_one(
            {"Medicine Name": {"$regex": f"^{medicine_name}$", "$options": "i"}}, 
            {"_id": 0}
        )
        print(f" Medicine search result: {medicine_data}")

        if medicine_data:
            medicines.append(medicine_data)

    print(f" Final results: {medicines}")

    return render_template("medicine.html", results=medicines)




from flask import request, jsonify
from flask_login import login_required
from .chatbot import get_chatbot_response  # Import chatbot function

@routes_bp.route("/chatbot", methods=["GET", "POST"])
@csrf.exempt  
@login_required
def chatbot():
    if request.method == "GET":
        return render_template("chatbot.html")  

    if request.method == "POST":
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400  
        
        user_message = data.get("message").strip()
        
        if not user_message:
            return jsonify({"error": "Empty message received"}), 400  
        
        bot_reply = get_chatbot_response(user_message)
        return jsonify({"reply": bot_reply}), 200


@routes_bp.route("/about")
def about():
    return render_template("about.html")


@routes_bp.route('/autocomplete', methods=["GET"])
@login_required
def autocomplete():
    query = request.args.get("query", "").strip()
    search_type = request.args.get("type", "")  # "medicine" or "disease"

    if not query:
        return jsonify([])  # Return empty list if no input

    regex_pattern = re.escape(query)  # Escape special characters
    regex_query = {"$regex": f"^{regex_pattern}", "$options": "i"}  # Case-insensitive regex

    if search_type == "medicine":
        results = mongo.db.medicine_details.find({"Medicine Name": regex_query}, {"Medicine Name": 1, "_id": 0})
    elif search_type == "disease":
        results = mongo.db.drug_disease.find({"disease": regex_query}, {"disease": 1, "_id": 0})
    else:
        return jsonify([])  # Invalid type

    # Convert results to a list of names
    suggestions = [result.get("Medicine Name") or result.get("disease") for result in results]
    return jsonify(suggestions)


