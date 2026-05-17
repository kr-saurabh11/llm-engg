# 1. Every call to an LLM is stateless
# 2. We pass in the entire conversation so far in the input prompt, every time
# 3. This gives the illusion that the LLM has memory - it apparently keeps the context of the conversation
# 4. But this is a trick; it's a by-product of providing the entire conversation, every time
# 5. An LLM just predicts the most likely next tokens in the sequence; if that sequence contains "My name is Saurabh" and later "What's my name?" then it will predict.. Saurabh!

from openai import OpenAI

url = 'http://localhost:11434/v1'
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Saurabh!"}
]
openai = OpenAI(base_url=url, api_key='ollama')
response = openai.chat.completions.create(model="llama3.2:1b", messages=messages)

print(response.choices[0].message.content)

# follow-up question
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
]

response = openai.chat.completions.create(model="llama3.2:1b", messages=messages)

# Every call to an LLM is completely STATELESS. It's a totally new call, every single time
print(response.choices[0].message.content)

# As AI engineers, it's OUR JOB to devise techniques to give the impression that the LLM has a "memory".
# We pass in the entire conversation so far in the input prompt, every time
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Saurabh!"},
    {"role": "assistant", "content": "Hi Saurabh! How can I assist you today?"},
    {"role": "user", "content": "What's my name?"}
]

response = openai.chat.completions.create(model="llama3.2:1b", messages=messages)

# This gives the illusion that the LLM has memory - it apparently keeps the context of the conversation
print(response.choices[0].message.content)
