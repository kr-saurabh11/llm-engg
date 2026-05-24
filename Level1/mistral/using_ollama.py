from ollama import chat

response = chat(
    model='mistral:7b',
    messages=[{'role': 'user', 'content': 'Hello!'}],
)
print(response.message.content)