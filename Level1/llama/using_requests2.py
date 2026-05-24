import requests
import json

url = 'http://localhost:11434/api/chat'

payload = {
    "model": "llama3.2:1b",
    "messages": [
        {"role": "system", "content": "You are a experienced computer science professor"},
        {"role": "user", "content": "What is python?"}
    ],
    "stream": True
}

response = requests.post(url, json=payload, stream=True)

if response.status_code == 200:
    print("Streaming response from Ollama:\n")
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                json_data = json.loads(line)
                if "message" in json_data and "content" in json_data["message"]:
                    content = json_data["message"]["content"]
                    print(content, end="", flush=True)
            except json.JSONDecodeError as e:
                print(f"\nFailed to parse line: {line}")
    print("\n")
else:
    print(f"Failed to stream response from Ollama: Status {response.status_code}")

