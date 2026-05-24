import os
import tempfile
from io import BytesIO

import gradio as gr
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv(override=True)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")

MODEL_OPTIONS = [
    "black-forest-labs/FLUX.1-schnell"
]

STYLE_OPTIONS = [
    "Anime",
    "Pop Art",
    "Cyberpunk",
    "Watercolor",
    "Ghibli Style Art"
]

HF_URL = "https://router.huggingface.co/hf-inference/models/{}"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
})


def generate_image(prompt: str, model: str, style: str):

    final_prompt = f"{prompt}, rendered in {style} style"

    try:
        response = session.post(
            HF_URL.format(model),
            json={"inputs": final_prompt},
            timeout=180
        )

        response.raise_for_status()

        image = Image.open(
            BytesIO(response.content)
        )

        # Save to temp file for download
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        image.save(temp_file.name)

        return image, temp_file.name

    except Exception as e:
        raise gr.Error(
            f"Generation failed: {str(e)}"
        )


theme = gr.themes.Citrus()

with gr.Blocks(
    title="Free Image Generator",
    theme=theme
) as demo:

    gr.Markdown("# 🎨 AI Image Generator")

    prompt = gr.Textbox(
        label="Prompt",
        placeholder="Astronaut riding horse on Mars..."
    )

    with gr.Row():

        model = gr.Dropdown(
            MODEL_OPTIONS,
            label="Model",
            value=MODEL_OPTIONS[0]
        )

        style = gr.Dropdown(
            STYLE_OPTIONS,
            label="Style",
            value="Anime"
        )

    generate_btn = gr.Button(
        "Generate"
    )

    output_image = gr.Image(
        type="pil",
        height=500,
        label="Generated Image"
    )

    download_file = gr.File(
        label="Download Image"
    )

    generate_btn.click(
        fn=generate_image,
        inputs=[prompt, model, style],
        outputs=[output_image, download_file]
    )

demo.launch(inbrowser=True)