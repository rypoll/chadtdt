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
    # Commented out: Extract the token from the request headers
    # token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    
    user_id = 'admin'  # Hardcoded for testing
    
    # Commented out: Verify the token
    # try:
    #     decoded_token = auth.verify_id_token(token)
    #     user_id = decoded_token['uid']
    # except Exception as e:
    #     return {"error": f"Invalid token or unauthorized: {str(e)}"}, 401

    # Check Firestore for user_id
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    print("User Doc:", user_doc.to_dict())  # Debugging line

    if not user_doc.exists:
        return {"error": "User not authorized"}, 403

    # Get OpenAI API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')

    # Configure OpenAI API key
    openai.api_key = api_key

    # Extract messages from request
    request_json = request.get_json()
    messages = request_json['messages']

    # Check Firestore for user's API call count
    if user_doc.exists:
        api_calls = user_doc.to_dict().get('api_calls', 0)
    else:
        api_calls = 0
        user_ref.set({'api_calls': api_calls})

    # Check if user has exceeded API call limit
    if api_calls >= 300:
        return {"error": "API call limit reached"}, 429

    try:
        response = get_response(messages)

        # Increment API call count in Firestore
        user_ref.update({'api_calls': firestore.Increment(1)})

        return response
    except Exception as e:
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
