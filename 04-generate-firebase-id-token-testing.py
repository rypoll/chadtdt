import requests
import json

# Your cloud function URL
url = "https://us-central1-autoflirt-401111.cloudfunctions.net/openai_proxy"

# Sample data to send in the request
data = {
    "messages": [
        {"role": "user", "content": "Who won the world series in 2020?"}
    ]
}

# Make the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Success:", json.dumps(response.json(), indent=4))
else:
    print("Failed:", response.content)
