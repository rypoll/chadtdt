from datetime import datetime, timedelta, timezone
import openai
import os
import json
import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth

# Initialize Firestore
firebase_admin.initialize_app()
db = firestore.client()

def openai_proxy(request):
    # Extract the token from the request header
    token = request.headers.get('Authorization')
    print("Received token:", token)  # Add this line
    if not token:
        return {"error": "Token is missing"}, 401

    # Verify the token and get the user's UID
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']
        print("Decoded user ID:", user_id)
    except Exception as e:
        print("Token verification failed:", str(e))
        return {"error": "Invalid token"}, 401

    # Check Firestore for user_id
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return {"error": "User not authorized"}, 403

    # Extract existing user data or initialize with default values
    user_data = user_doc.to_dict() if user_doc.exists else {}
    api_calls = user_data.get('api_calls', 0)
    last_reset = user_data.get('last_reset', datetime.now(timezone.utc))  # Make timezone-aware
    last_request_time = user_data.get('last_request_time', datetime.now(timezone.utc))  # Make timezone-aware
    requests_in_last_minute = user_data.get('requests_in_last_minute', 0)

    # Check if a month has passed since the last reset
    if datetime.now(timezone.utc) >= last_reset + timedelta(days=30):  # Make timezone-aware
        api_calls = 0  # Reset the API call count
        last_reset = datetime.now(timezone.utc)  # Make timezone-aware

    # Check if a minute has passed since the last request
    if datetime.now(timezone.utc) >= last_request_time + timedelta(minutes=1):  # Make timezone-aware
        requests_in_last_minute = 0  # Reset the request count for the last minute

    # Check if user has exceeded API call limit
    if api_calls >= 900:
        return {"error": "API call limit reached"}, 429

    # Check if user has exceeded rate limit of 10 requests per minute
    if requests_in_last_minute >= 60:
        return {"error": "Rate limit exceeded"}, 429

    # Get OpenAI API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')

    # Configure OpenAI API key
    openai.api_key = api_key

    # Extract messages from request
    try:
        request_json = request.get_json()
        messages = request_json['messages']
        response = get_response(messages)

        print(f"Requests in last minute before increment: {requests_in_last_minute}")

        # After incrementing requests_in_last_minute
        user_ref.set({
                'api_calls': firestore.Increment(1),
                'last_reset': last_reset,
                'last_request_time': datetime.now(timezone.utc),  # Make timezone-aware
                'requests_in_last_minute': firestore.Increment(1)
            }, merge=True)
        print(f"Requests in last minute after increment: {requests_in_last_minute + 1}")

        return response
    except Exception as e:
        print("Exception:", str(e))  # Add this line
        return {"error": str(e)}, 500



def get_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response
    except Exception as e:
        if "maximum context length" in str(e):
            print("Token count exceeds the standard limit. Switching to gpt-3.5-turbo-16k.")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages
            )
            return response
        else:
            raise e
