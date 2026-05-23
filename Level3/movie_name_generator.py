import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
hf_token = os.getenv('HF_TOKEN')
if hf_token:
    print(f"HF_TOKEN exists and begins {hf_token[:2]}")
else:
    print("HF_TOKEN not set (and this is optional)")

client = OpenAI(
    api_key=hf_token,
    base_url="https://router.huggingface.co/v1"
)

def prompt_builder(theme, language):
    system_prompt = f"""
        You are a movie title expert.
        You generate movie titles based on the given theme and language.
        Generate realistic movie titles only.
        The movie titles should be in {language}.
        The movie should be short and catchy.
        Generate upto 10 movie titles.
        No explanations.
        
        Example 1: Theme = animal
        The movie title generated should be like
        Anaconda
        Snakes on a Plane
        Jaws
        Hotel for Dogs
        Beverly Hills Chihuahua
        Good Boy!
        101 Dalmatians
        Never Cry Wolf
        The Doberman Gang
        Dolphin Tale
        
        Example 2: Theme = history
        The movie title generated should be like
        Saving Private Ryan
        Gladiator
        Schindler's List
        Blood Diamond
        Black Hawk Down
        The Last of the Mohicans
        Braveheart
        Apollo 13
        """

    user_prompt = f"""
        Suggest movie titles for the theme: {theme} and language: {language}
        """

    return system_prompt, user_prompt


def call_llm(model,theme, language):
    system_prompt, user_prompt = prompt_builder(theme, language)
    response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    )
    return response.choices[0].message.content.strip()

#call_llm(theme="animal", language="Hindi")

def run_app():
    with gr.Blocks(title="Movie name generator") as demo:
        gr.Markdown("# Generates Movie names")

        model = gr.Dropdown(
            ["meta-llama/Llama-3.3-70B-Instruct", "deepseek-ai/DeepSeek-V4-Pro",
             "openai/gpt-oss-120b", "Qwen/QwQ-32B"],
            label="Select Model",
            value="meta-llama/Llama-3.3-70B-Instruct"
        )
        language = gr.Dropdown(
            ["English", "Hindi", "Spanish", "French"],
            label="Select Language",
            value="English"
        )
        theme = gr.Textbox(label="Enter Theme", lines=1)
        output = gr.Textbox(label="Generated Movie Names", lines=10)
        generate_btn = gr.Button("Generate Names")

        generate_btn.click(fn=call_llm, inputs=[model,theme,language], outputs=output)
        grtheme = gr.themes.Citrus()
    demo.launch(inbrowser=True,theme=grtheme)

run_app()