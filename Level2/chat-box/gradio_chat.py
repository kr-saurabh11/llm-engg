from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(api_key=google_api_key, base_url=gemini_url)

MODEL = "gemini-3.1-flash-lite"
system_message = "You are a helpful assistant"

def chat(message, history):
    return f"You said {message} and the history is {history} but I still say bananas"

gr.ChatInterface(fn=chat).launch()