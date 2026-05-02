import requests
import json

url = 'http://localhost:11434/api/chat'

payload = {"model": "llama3.2:1b",
           "messages": [
               {"role": "system", "content": "You are a experienced computer science professor"},
               {"role": "user", "content": "What is python?"}
           ]}
response = requests.post(url, json=payload, stream=True)

#print(response)

if response.status_code == 200:
    print("streaming response from ollama:")
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                json_data = json.loads(line)
                if "message" in json_data and "content" in json_data["message"]:
                    print(json_data["message"]["content"], end="")
            except json.JSONDecodeError:
                print(f"\n Failed to parse line: {line}")
    print()
else:
    print(f"Failed to stream response from ollama: {response.status_code}")

