from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    # model="openai/gpt-5.4-image-2",
    model="openai/gpt-5-image-mini",
    messages=[
        {
            "role": "user",
            "content": "Generate a beautiful sunset over mountains"
        }
    ],
    extra_body={"modalities": ["image", "text"]},
    max_tokens=1333
)

message = response.choices[0].message

if hasattr(message, "images") and message.images:
    for i, image in enumerate(message.images):

        data_url = image["image_url"]["url"]

        # Remove: data:image/png;base64,
        base64_data = data_url.split(",")[1]

        image_bytes = base64.b64decode(base64_data)

        filename = f"generated_{i}.png"

        with open(filename, "wb") as f:
            f.write(image_bytes)

        print("Saved:", filename)