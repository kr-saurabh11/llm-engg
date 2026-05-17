from openai import OpenAI

system_prompt = """
You are a hindi teacher. You need to explain in hindi on how the calculation is working
"""

messages = [
    {"role": "system", "content":  system_prompt},
    {"role": "user", "content": "What is 2 + 2*6//4?"}
]

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
response = openai.chat.completions.create(model="llama3.2:1b", messages=messages)

print(response.choices[0].message.content)