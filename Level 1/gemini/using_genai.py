from google import genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')

client = genai.Client(api_key=google_api_key)

response = client.models.generate_content(
    model="gemma-4-31b-it", # Do not include the colon or 'models/' prefix when using the modern SDK
    contents="Hello Gemma!",
)
print(response.text)