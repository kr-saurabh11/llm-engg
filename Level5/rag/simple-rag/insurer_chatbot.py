import os
import glob
from dotenv import load_dotenv
from pathlib import Path
import gradio as gr
from openai import OpenAI
from commons.response_sanitizer import sanitize_llm_response

# Setting up

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)
MODEL = "gemma-4-31b-it"
# MODEL = "gemini-3.5-flash"

knowledge = {}

filenames = glob.glob("../knowledge-base/employees/*")

for filename in filenames:
    name = Path(filename).stem.split(' ')[-1]
    with open(filename, "r", encoding="utf-8") as f:
        knowledge[name.lower()] = f.read()

filenames = glob.glob("../knowledge-base/products/*")

for filename in filenames:
    name = Path(filename).stem
    with open(filename, "r", encoding="utf-8") as f:
        knowledge[name.lower()] = f.read()

SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""

def get_relevant_context(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()
    relevant_context = []
    for word in words:
        if word in knowledge:
            relevant_context.append(knowledge[word])
    return relevant_context

def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        result = "There is no additional context relevant to the user's question."
    else:
        result = "The following additional context might be relevant in answering the user's question:\n\n"
        result += "\n\n".join(relevant_context)
    return result


def chat(message, history):
    system_message = SYSTEM_PREFIX + additional_context(message)
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    print(messages)
    response = gemini.chat.completions.create(model=MODEL, messages=messages)
    return sanitize_llm_response(response.choices[0].message.content)

view = gr.ChatInterface(chat).launch(inbrowser=True)