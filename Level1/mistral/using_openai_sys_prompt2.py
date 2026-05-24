from openai import OpenAI

system_prompt = """
You are a music teacher. You need to explain as a teacher on how the calculation is working
"""

messages = [
    {"role": "system", "content":  system_prompt},
    {"role": "user", "content": "What is 2 + 2*6//4?"}
]

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
response = openai.chat.completions.create(model="mistral:7b", messages=messages)

print(response.choices[0].message.content)