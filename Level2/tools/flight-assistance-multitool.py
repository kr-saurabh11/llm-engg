from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv
import json

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(api_key=google_api_key, base_url=gemini_url)

MODEL = "gemini-2.5-flash"
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


def handle_tool_call(message):
    print("Number of tool calls:", len(message.tool_calls))
    responses = []
    for every_tool_call in message.tool_calls:
        print("Tool call is for function:", every_tool_call.function.name)
        arguments = json.loads(every_tool_call.function.arguments)
        if every_tool_call.function.name == "get_ticket_price":
            responses.append(handle_price_tool_call(every_tool_call.id, arguments))
        elif every_tool_call.function.name == "get_flight_schedules":
            responses.append(handle_schedule_tool_call(every_tool_call.id, arguments))
        elif every_tool_call.function.name == "flight_confirmation_number":
            responses.append(handle_confirmation_tool_call(every_tool_call.id, arguments))
    print("handle_tool_call is returning responses:", responses)
    return responses


def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        responses = handle_tool_call(message)
        messages.append(message)
        messages = messages + responses
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content

gr.ChatInterface(fn=chat).launch(inbrowser=True)
