from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)

google_api_key = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Safer logging
print(f"GOOGLE_API_KEY: {google_api_key[:4]}..." if google_api_key else "Missing")
print(f"GROQ_API_KEY: {groq_api_key[:4]}..." if groq_api_key else "Missing")
print(f"OPENROUTER_API_KEY: {openrouter_api_key[:4]}..." if openrouter_api_key else "Missing")

# Google Gemini OpenAI compatibility endpoint
gemini = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Groq OpenAI compatibility endpoint
groq = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# OpenRouter endpoint
openrouter = OpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

message = "Hello! This is my first ever message to you! Hi!"
messages = [
    {
        "role": "user",
        "content": message
    }
]


def ask_gemini(client, model, provider):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        print(f"\n=== {provider} ===")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"\n=== {provider} ERROR ===")
        print(e)


def ask_groq(client, model, provider):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=7000,
            reasoning_effort="medium"
        )

        print(f"\n=== {provider} ===")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"\n=== {provider} ERROR ===")
        print(e)


def ask_openrouter(client, model, provider):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1333,
            reasoning_effort="medium"
        )

        print(f"\n=== {provider} ===")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"\n=== {provider} ERROR ===")
        print(e)


ask_gemini(
    gemini,
    "gemini-2.5-flash-lite",
    "Gemini"
)

ask_groq(
    groq,
    "openai/gpt-oss-120b",
    "Groq"
)

ask_openrouter(
    openrouter,
    "openai/gpt-4o",
    "OpenRouter"
)
