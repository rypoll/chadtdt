import requests
import json

try:
    with open('../token.json', 'r') as f:
        data = json.load(f)
        token = data['idToken']
    print("Using token:", token)
except FileNotFoundError:
    print("Token file not found.")
    exit()

headers = {'Authorization': token}
    
temp_system_message = "You are 'A'. Give a flirty response to 'G' in this conversation"
formatted_text2 = """
A: Hey
G: Hi there
"""

content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)
messages = [{"role": "user", "content": content}]
url = "https://us-central1-autoflirt-401111.cloudfunctions.net/openai_proxy"
data = {"messages": messages}

response = requests.post(url, headers=headers, json=data)
response_json = response.json()

if response.status_code == 200:
    print("Success:", json.dumps(response.json(), indent=4))
    try:
        print(response_json['choices'][0]['message']['content'])
    except KeyError:
        print("Expected field not found in response.")
else:
    print("Failed:", response.content)

print("Raw Response:", response.content)
print(response_json['choices'][0]['message']['content'])