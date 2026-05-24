from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
print(f'GOOGLE_API_KEY:{google_api_key}')

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

message = "Hello, Google! This is my first ever message to you! Hi!"
messages = [{"role": "user", "content": message}]

# response = gemini.chat.completions.create(model="gemini-2.5-flash", messages=messages)
# response = gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=messages)
# response = gemini.chat.completions.create(model="gemini-3-flash-preview", messages=messages)
# response = gemini.chat.completions.create(model="gemini-3.1-flash-lite", messages=messages)
response = gemini.chat.completions.create(model="gemma-4-31b-it", messages=messages)


print(response.choices[0].message.content)