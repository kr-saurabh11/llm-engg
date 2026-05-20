import os
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types
import gradio as gr
import wave
import tempfile
import sqlite3
import json

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(api_key=google_api_key, base_url=gemini_url)
genaiClient = genai.Client()

MODEL = "gemini-3.1-flash-lite"
# AUDIO_MODEL = "gemini-2.5-flash-preview-tts"
AUDIO_MODEL = "gemini-3.1-flash-tts-preview"
DB = "prices.db"

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
        result = cursor.fetchone()
        return f"Ticket price to {city} is {result[0]}" if result else "No price data available for this city"

print(get_ticket_price("Paris"))

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]

def talker(message):
    response = genaiClient.models.generate_content(
        model=AUDIO_MODEL,
        contents=message,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            )
        )
    )

    # Extract raw PCM bytes
    audio_bytes = response.candidates[0].content.parts[0].inline_data.data

    # Create temp wav file
    temp = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    with wave.open(temp.name, "wb") as wav_file:
        wav_file.setnchannels(1)      # mono
        wav_file.setsampwidth(2)      # 16-bit PCM
        wav_file.setframerate(24000)  # from mime type
        wav_file.writeframes(audio_bytes)

    return temp.name


def chat(history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        responses, cities = handle_tool_calls_and_return_cities(message)
        messages.append(message)
        messages.extend(responses)
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    reply = response.choices[0].message.content
    history += [{"role": "assistant", "content": reply}]

    voice = talker(reply)
    return history, voice

def handle_tool_calls_and_return_cities(message):
    responses = []
    cities = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            cities.append(city)
            price_details = get_ticket_price(city)
            responses.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id
            })
    return responses, cities

# Callbacks (along with the chat() function above)
def put_message_in_chatbot(message, history):
        return "", history + [{"role":"user", "content":message}]

# UI definition
with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500)
    with gr.Row():
        audio_output = gr.Audio(autoplay=True)
    with gr.Row():
        message = gr.Textbox(label="Chat with our AI Assistant:")
    # Hooking up events to callbacks
    message.submit(put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]).then(
        chat, inputs=chatbot, outputs=[chatbot, audio_output]
    )

ui.launch(inbrowser=True)