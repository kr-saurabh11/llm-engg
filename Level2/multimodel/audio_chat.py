import os
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types
import gradio as gr
import wave
import tempfile

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(api_key=google_api_key, base_url=gemini_url)
genaiClient = genai.Client()

MODEL = "gemini-3.1-flash-lite"
# AUDIO_MODEL = "gemini-2.5-flash-preview-tts"
AUDIO_MODEL = "gemini-3.1-flash-tts-preview"

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
    messages = history
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    reply = response.choices[0].message.content
    print(reply)
    history += [{"role": "assistant", "content": reply}]
    voice = talker(reply)
    return history, voice

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