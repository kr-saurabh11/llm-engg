import requests

url = 'http://localhost:11434/api/chat'
api_key = '' #use this for paid LLMs
headers = {'Authorization':f'Bearer {api_key}','Content-Type': 'application/json'}


payload = {
    "model": "llama3.2:1b",
    "messages": [
        {"role": "system", "content": "You are a experienced computer science professor"},
        {"role": "user", "content": "What is python?"}
    ],
    "stream": False
}

response = requests.post(url,headers=headers, json=payload)

print(response.json())


