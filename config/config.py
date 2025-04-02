import os
import json

# Get the absolute path of the config folder
config_path = os.path.join(os.path.dirname(__file__), "secret_config.json")

# Load sensitive data from `secret_config.json`
with open(config_path) as config_file:
    config_data = json.load(config_file)

class Config:
    SECRET_KEY = config_data.get("SECRET_KEY", "default_secret_key")  # Flask security key
    MONGO_URI = config_data.get("MONGO_URI", "mongodb://localhost:27017/healthcare_db")  # MongoDB connection
    LLM_API_KEY = config_data.get("LLM_API_KEY", "")  # API Key for chatbot
    DEBUG = True  # Enable debug mode for development

class ProductionConfig(Config):
    DEBUG = False  # Disable debug mode in production

class DevelopmentConfig(Config):
    DEBUG = True  # Enable debug mode in development

# ✅ Choose configuration based on environment
config = DevelopmentConfig() if os.getenv("FLASK_ENV") == "development" else ProductionConfig()
