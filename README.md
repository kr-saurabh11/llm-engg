# LLM Engineering - Learning & Demo Project

A hands-on project for learning and exploring Large Language Models (LLMs) with practical examples using Ollama, OpenAI SDK, and HTTP requests.

## Overview

This project demonstrates multiple approaches to interact with LLMs:
- **Local LLM Execution** using Ollama
- **Chat Completions** using the OpenAI-compatible API
- **HTTP Streaming Requests** for real-time responses
- **System Prompts** for customized AI behavior

## Features

- 🦙 **Ollama Integration** - Run LLMs locally
- 🔌 **OpenAI SDK** - Compatible with Ollama's OpenAI-compatible endpoint
- 📡 **HTTP Streaming** - Stream responses for real-time interaction
- 💬 **System Prompts** - Control AI behavior with custom instructions
- 🐍 **Python 3.12+** - Modern Python with type hints

## Prerequisites

- **Python 3.12** or higher
- **Ollama** - To run LLMs locally
- **uv** - Fast Python package installer (optional but recommended)

## Installation

### 1. Install Ollama

Download and install Ollama from [ollama.com](https://ollama.com):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify installation:
```bash
ollama --version
```

### 2. Install uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:
```bash
uv --version
```

### 3. Clone and Setup Project

```bash
cd /path/to/llm-engg
uv sync
```

Alternatively, using pip:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

## Quick Start

### 1. Start Ollama Server

Pull and run the Llama 3.2 model:

```bash
ollama run llama3.2:1b
```

This will:
- Download the Llama 3.2 1B model (if not already downloaded)
- Start the local server on `http://localhost:11434`

### 2. Run Examples

#### Basic Chat with OpenAI SDK

```bash
cd llama/level1
python hello.py
```

#### Using Ollama's Native SDK

```bash
python using_ollama.py
```

#### Streaming with HTTP Requests

```bash
python using_requests2.py
```

#### System Prompts Examples

```bash
python using_openai_sys_prompt1.py
python using_openai_sys_prompt2.py
python using_openai_sys_prompt3.py
```

## Project Structure

```
llm-engg/
├── README.md              # This file
├── SETUP.md              # Detailed setup instructions
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
├── uv.lock              # Dependency lock file
├── .env                 # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── llama/
    └── level1/
        ├── hello.py                      # Basic chat example
        ├── using_ollama.py               # Ollama SDK example
        ├── using_openai_sys_prompt1.py   # System prompt example 1
        ├── using_openai_sys_prompt2.py   # System prompt example 2
        ├── using_openai_sys_prompt3.py   # System prompt example 3
        └── using_requests.py             # HTTP streaming example
```

## Dependencies

### Core LLM Libraries
- **ollama** - Official Ollama SDK for Python
- **openai** - OpenAI Python client (compatible with Ollama's API)
- **requests** - HTTP library for manual API calls

### Data Science & ML
- **langchain** - LLM application framework
- **transformers** - HuggingFace transformers library
- **langchain-community** - Community integrations

### AI Provider SDKs
- **google-generativeai** - Google's Generative AI API
- **anthropic** - Anthropic's Claude API

### Utilities
- **python-dotenv** - Load environment variables
- **jupyter**-related - Jupyter notebooks support
- **chromadb** - Vector database for embeddings
- **beautifulsoup4** - Web scraping

See `requirements.txt` for complete list.

## API Endpoints

### Ollama OpenAI-Compatible Endpoint
```
POST http://localhost:11434/v1/chat/completions
```

### Ollama Native Endpoint
```
POST http://localhost:11434/api/chat
```

## Example Usage

### Using OpenAI SDK with Ollama

```python
from openai import OpenAI

openai = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

response = openai.chat.completions.create(
    model="llama3.2:1b",
    messages=[
        {"role": "user", "content": "Hello, llama!"}
    ]
)

print(response.choices[0].message.content)
```

### Using Ollama SDK

```python
from ollama import chat

response = chat(
    model='llama3.2:1b',
    messages=[{'role': 'user', 'content': 'Hello!'}]
)

print(response.message.content)
```

### Using HTTP Streaming

```python
import requests
import json

response = requests.post(
    'http://localhost:11434/api/chat',
    json={
        "model": "llama3.2:1b",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(json.loads(line)['message']['content'], end="")
```

## Troubleshooting

### Ollama Connection Error
Ensure Ollama is running:
```bash
ollama run llama3.2:1b
```

### Model Not Found
Download the model first:
```bash
ollama pull llama3.2:1b
```

### Port Already in Use
Ollama defaults to port 11434. Check if it's already running or use a different port.

### Import Errors
Ensure all dependencies are installed:
```bash
uv sync
# or
pip install -r requirements.txt
```

## Learning Path

1. **Start with** `hello.py` - Basic chat completion
2. **Explore** `using_ollama.py` - Native SDK usage
3. **Try** `using_requests.py` - Raw HTTP handling and streaming
4. **Study** `using_openai_sys_prompt*.py` - System prompts and AI control

## Available Models

Check available models and their sizes:

```bash
ollama list
```

Common lightweight models for local development:
- `llama3.2:1b` - 1 Billion parameters (very fast, lower quality)
- `llama3.2:3b` - 3 Billion parameters (balanced)
- `mistral:latest` - Fast and efficient

See [Ollama Models](https://ollama.com/library) for more options.

## Environment Variables

Create or update `.env` file:

```env
OPENAI_API_KEY=your_key_here  # Optional, not needed for local Ollama
```

⚠️ **Important**: The `.env` file is in `.gitignore` and won't be committed to version control.

## Performance Tips

- Start with smaller models like `llama3.2:1b` for faster responses
- Use streaming for better UX with larger models
- Set `stream=True` in requests for real-time output
- Use appropriate system prompts to reduce token usage

## Additional Resources

- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Documentation](https://python.langchain.com/)

## License

This is a learning project. Modify and use as needed for your studies.

## Contributing

Feel free to add more examples and improvements to this learning project!

---

**Last Updated**: May 2, 2026
