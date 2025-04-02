import google.generativeai as genai
import json

# Load API key from the config file
config_path = "C:/Users/Hp/Desktop/healthcare/config/secret_config.json"

try:
    with open(config_path, "r") as f:
        config = json.load(f)
        api_key = config.get("API_KEY")

    if not api_key:
        raise ValueError("API key is missing in secret_config.json")

    # Configure Gemini API
    genai.configure(api_key=api_key)

    # Initialize the model
    model = genai.GenerativeModel("gemini-2.0-flash")

except Exception as e:
    print("Error initializing chatbot:", e)
    model = None  # Prevent crashes

def get_chatbot_response(user_input):
    """
    Generates a response using the Gemini model.
    
    :param user_input: The message from the user.
    :return: Response from the chatbot.
    """
    if not model:
        return "Chatbot is currently unavailable."

    try:
        response = model.generate_content(user_input)
        return response.text  # Return the chatbot's response
    except Exception as e:
        return f"Error: {e}"
