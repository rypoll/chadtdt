import openai
import os
import json

def openai_proxy(request):
    request_json = request.get_json()
    messages = request_json['messages']

    # Get OpenAI API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')

    # Configure OpenAI API key
    openai.api_key = api_key

    try:
        response = get_response(messages)
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
