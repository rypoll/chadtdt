import requests
import json


temp_system_message = "You are 'A'. Give a flirty response to 'G' in this conversation"
formatted_text2 = """
A: Hey
G: Hi there
"""


content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)

messages = [{"role": "user", "content": content}]


url = "https://us-central1-autoflirt-401111.cloudfunctions.net/openai_proxy"

data = {
    "messages": messages  # Use the mock messages variable here
}

response = requests.post(url, json=data)

response_json = response.json()
#print(response_json['choices'][0]['message']['content'])
#print(response['choices'][0]['message']['content'])