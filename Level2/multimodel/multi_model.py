import os
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import base64
from io import BytesIO
from PIL import Image
from IPython.display import display



load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(api_key=google_api_key, base_url=gemini_url)
genaiClient = genai.Client(api_key=google_api_key)

DB = "prices.db"
MODEL = "gemini-3.1-flash-lite"
IMAGE_MODEL = "gemini-2.5-flash-image"
# IMAGE_MODEL = "gemini-3.1-flash-image-preview"

def artist_openai(city):
    print(f"Generating image for {city} using model {IMAGE_MODEL}")
    response = openai.images.generate(
        model=IMAGE_MODEL,
        prompt=(
            f"An image representing a vacation in {city}, "
            f"showing tourist spots and everything unique "
            f"about {city}, in a vibrant pop-art style"
        ),
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return Image.open(BytesIO(image_bytes))

def artist_genai(city):
    print(f"Generating image for {city} using model {IMAGE_MODEL}")
    response = genaiClient.models.generate_content(
        model='gemini-3.1-flash-image-preview',
        contents=(
            f"An image representing a vacation in {city}, "
            f"showing tourist spots and everything unique "
            f"about {city}, in a vibrant pop-art style"
        )
    )
    # Extract image from returned parts
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            image_bytes = part.inline_data.data
            return Image.open(BytesIO(image_bytes))

    raise Exception("No image returned")


image1 = artist_openai("New York City")
image2 = artist_genai("New York City")
display(image1)
display(image2)


