from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

print(f'OPENAI_API_KEY:{api_key}')

message = "Hello, llama! This is my first ever message to you! Hi!"
messages = [{"role": "user", "content": message}]

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
response = openai.chat.completions.create(model="llama3.2:1b", messages=messages)  # type: ignore

print(response.choices[0].message.content)