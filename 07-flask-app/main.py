from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import auth
import requests  # Import the requests library
from dotenv import load_dotenv
load_dotenv()

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")  # Replace with your Firebase Web API Key

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    # Verify email and password using Firebase REST API
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        try:
            user_data = response.json()
            user = auth.get_user_by_email(email)
            custom_token = auth.create_custom_token(user.uid)
            return jsonify({"token": custom_token.decode()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Invalid email or password"}), 400
