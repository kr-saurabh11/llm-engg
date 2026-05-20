import os
from dotenv import load_dotenv
from google import genai
from IPython.display import Audio
from google.genai import types
import wave

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
genaiClient = genai.Client()


def talker(message):
    response = genaiClient.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
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
    audio_bytes = response.candidates[0].content.parts[0].inline_data.data
    return audio_bytes

def save_audio(audio_bytes, filename="speech.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)      # channels=1
        wf.setsampwidth(2)      # 16-bit = 2 bytes
        wf.setframerate(24000)  # rate=24000
        wf.writeframes(audio_bytes)

    return filename

audio = talker("Welcome to New York City, it is place for rich and actors")
file = save_audio(audio)

Audio(file)