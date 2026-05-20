from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv
import json
from google import genai
from google.genai import types
import wave
import tempfile



load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(api_key=google_api_key, base_url=gemini_url)
genaiClient = genai.Client()

MODEL = "gemini-3.1-flash-lite"
AUDIO_MODEL = "gemini-3.1-flash-tts-preview"

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
flight_schedules = {"london": ["08:00", "15:00"], "paris": ["09:00", "16:00"], "tokyo": ["12:00"],
                    "berlin": ["07:00", "13:00"]}


def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")


def get_flight_schedules(destination_city):
    print(f"Tool get_flight_hours called for {destination_city}")
    city = destination_city.lower()
    return flight_schedules.get(city, "Unknown")


def flight_confirmation_number(destination_city, date, hour):
    import random
    number = destination_city[:3].upper() + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    print(f"Tool flight_confirmation_number called for {destination_city} on {date} at {hour}, returning {number}")
    return number


print(get_ticket_price("London"))
print(get_flight_schedules("London"))
print(flight_confirmation_number("London", "2024-10-01", "15:00"))

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need \
        to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
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

schedule_function = {
    "name": "get_flight_schedules",
    "description": "Get the daily flight schedules (departure times) to the destination city. Call this \
        whenever you need to know the flight times, for example when a customer asks 'What time \
        are the flights to this city?'",
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

confirmation_function = {
    "name": "flight_confirmation_number",
    "description": "Get a flight confirmation number for a booking. Call this whenever you need to \
        provide a confirmation number, after a customer has selected a destination city, a flight \
        date and a departure time, and also asked for the price. For example when a customer says \
        'I'd like to book that flight'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
            "date": {
                "type": "string",
                "description": "The date of the flight, in YYYY-MM-DD format",
            },
            "hour": {
                "type": "string",
                "description": "The departure time of the flight, in HH:MM format",
            },
        },
        "required": ["destination_city", "date", "hour"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function},
         {"type": "function", "function": schedule_function},
         {"type": "function", "function": confirmation_function}]


def handle_price_tool_call(tool_call_id, arguments):
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call_id
    }
    print("handle_price_tool_call is returning response:", response)
    return response


def handle_schedule_tool_call(tool_call_id, arguments):
    city = arguments.get('destination_city')
    schedules = get_flight_schedules(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "schedules": schedules}),
        "tool_call_id": tool_call_id
    }
    print("handle_schedule_tool_call is returning response:", response)
    return response


def handle_confirmation_tool_call(tool_call_id, arguments):
    city = arguments.get('destination_city')
    date = arguments.get('date')
    hour = arguments.get('hour')
    confirmation = flight_confirmation_number(city, date, hour)
    response = {
        "role": "tool",
        "content": json.dumps(
            {"destination_city": city, "date": date, "hour": hour, "confirmation_number": confirmation}),
        "tool_call_id": tool_call_id
    }
    print("handle_confirmation_tool_call is returning response:", response)
    return response


def handle_tool_call(called_tool):
    print("Tool call is for function:", called_tool.function.name)
    arguments = json.loads(called_tool.function.arguments)
    if called_tool.function.name == "get_ticket_price":
        response = handle_price_tool_call(called_tool.id, arguments)
    elif called_tool.function.name == "get_flight_schedules":
        response = handle_schedule_tool_call(called_tool.id, arguments)
    elif called_tool.function.name == "flight_confirmation_number":
        response = handle_confirmation_tool_call(called_tool.id, arguments)
    return response


def chat(history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        messages.append(message)
        for each_tool_call in message.tool_calls:
            tool_response = handle_tool_call(each_tool_call)
            messages.append(tool_response)
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    reply = response.choices[0].message.content
    history += [{"role": "assistant", "content": reply}]

    voice = talker(reply)
    return history, voice

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
