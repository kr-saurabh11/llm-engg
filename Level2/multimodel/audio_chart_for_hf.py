import os
import tempfile
import wave
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types
import gradio as gr
import re

load_dotenv(override=True)

google_api_key = os.getenv("GOOGLE_API_KEY")

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

openai_client = OpenAI(
    api_key=google_api_key,
    base_url=gemini_url
)

genaiClient = genai.Client()

models = ["gemini-3.5-flash", "gemini-2.5-flash", "gemma-4-31b-it"]
AUDIO_MODEL = "gemini-3.1-flash-tts-preview"


def talker(message):
    response = genaiClient.models.generate_content(
        model=AUDIO_MODEL,
        contents=message,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=
                    types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            )
        )
    )

    audio_bytes = (
        response.candidates[0]
        .content.parts[0]
        .inline_data.data
    )

    temp = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    with wave.open(temp.name, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    return temp.name

def clean_response(text):
    if not text:
        return ""

    # Remove <thought>...</thought>
    text = re.sub(
        r"<thought>.*?</thought>",
        "",
        text,
        flags=re.DOTALL
    )

    # Remove any remaining XML-ish tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    return text.strip()

def chat(history, voice_enabled, model):
    messages = [
        {
            "role": h["role"],
            "content": h["content"]
        }
        for h in history
    ]
    stream = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    partial = ""
    history.append({
        "role":"assistant",
        "content":""
    })
    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            partial += token
            cleaned = clean_response(partial)
            history[-1]["content"] = cleaned
            yield history, None
    final_text = clean_response(partial)
    history[-1]["content"] = final_text
    voice = None
    if voice_enabled:
        voice = talker(final_text)
    yield history, voice


def put_message_in_chatbot(
        message,
        history
):

    return "", history + [
        {
            "role":"user",
            "content":message
        }
    ]


custom_css = """
footer{
visibility:hidden;
}

#title{
text-align:center;
}
"""

with gr.Blocks(
        title="AI Voice Assistant"
) as ui:

    gr.HTML("""
    <div id='title'>
    <h1>🎙️ AI Voice Assistant</h1>
    <p>Streaming chat + optional speech</p>
    </div>
    """)

    with gr.Row():
        model = gr.Dropdown(models, label="Select model", value=models[2])

    with gr.Row():

        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                height=650
            )
            with gr.Row():
                message = gr.Textbox(
                    placeholder=
                    "Ask anything...",
                    scale=8
                )
                send = gr.Button(
                    "🚀 Send",
                    variant="primary"
                )

        with gr.Column(scale=1):
            voice_enabled = gr.Checkbox(
                value=True,
                label="Enable voice"
            )

            audio_output = gr.Audio(
                autoplay=True,
                label="Speech"
            )

            clear = gr.Button(
                "🗑️ Clear"
            )

    message.submit(
        put_message_in_chatbot,
        [message, chatbot],
        [message, chatbot]
    ).then(
        chat,
        [chatbot, voice_enabled,model],
        [chatbot, audio_output]
    )

    send.click(
        put_message_in_chatbot,
        [message, chatbot],
        [message, chatbot]
    ).then(
        chat,
        [chatbot, voice_enabled],
        [chatbot, audio_output]
    )

    clear.click(
        lambda:([],None),
        outputs=[
            chatbot,
            audio_output
        ]
    )


ui.launch(
    theme=gr.themes.Ocean(),
    css=custom_css,
    inbrowser=True
)