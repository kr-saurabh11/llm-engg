from openai import OpenAI

message = "Hello, llama! This is my first ever message to you! Hi!"
messages = [{"role": "user", "content": message}]

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
response = openai.chat.completions.create(model="llama3.2:1b", messages=messages)
response.choices[0].message.content

print(response.choices[0].message.content)