# LLM Engineering - Learning & Demo Project

A hands-on project for learning and exploring Large Language Models (LLMs). This repository contains examples and utilities for:
- running local models with Ollama
- calling OpenAI-compatible endpoints
- performing streaming HTTP requests
- tokenization utilities and tokenizer fallbacks
- small Gradio demos and code-porting (Python -> C++ / Java) workflows

## Features

- 🦙 Ollama integration (local models)
- 🔌 OpenAI-compatible SDK usage (works with Ollama and cloud endpoints)
- 📡 HTTP streaming examples (line-delimited JSON / server-sent chunks)
- 🧩 Tokenization examples (Ollama tokenize endpoint + HuggingFace fallback)
- 🧰 Tools and function-calling examples (flight-assistance multitool)
- 🔁 Code-porting tools (Python -> C++ and Python -> Java examples) with compile/run helpers
- 🐍 Python 3.12+ examples and Gradio UIs

## Prerequisites

- Python 3.12 or higher
- Ollama (for local model execution) — optional if you only use cloud providers
- clang++ (for compiling generated C++ locally) or a Java 17 runtime/javac if using Java ports
- Recommended: uv (fast installer) or pip for dependencies

## Installation

### 1. Install Ollama (optional)

Install Ollama for local LLMs:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

### 2. Install dependencies

Recommended: use `uv` (fast installer) or `pip`.

Using uv (optional):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

Using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the project root and add keys you need (examples):

```env
GOOGLE_API_KEY=your_google_api_key_if_using_gemini
OPENROUTER_API_KEY=your_openrouter_key
GROQ_API_KEY=your_groq_key
HF_TOKEN=your_huggingface_token
# For Ollama local OpenAI-compatible SDK use api_key='ollama' (no value required in .env)
```

Note: `.env` is ignored by git in this repo.

Quick start

1. (Optional) Start Ollama and run a model locally:

```bash
ollama pull llama3.2:1b
ollama run llama3.2:1b
```

2. Run examples (from repository root):

- Basic chat (OpenAI-compatible SDK):

```bash
python llama/level1/hello.py
```

- Ollama native SDK example:

```bash
python llama/level1/using_ollama.py
```

- HTTP streaming examples (line-delimited JSON):

```bash
python llama/level1/using_requests2.py
```

- Tokenizer examples (Ollama tokenize endpoint and transformers fallback):

```bash
python "Level1/tokenizer/tokenizer_llama.py"
python "Level1/tokenizer/tokenizer_gpt.py"
```

- Code porting UI (Gradio):

```bash
python Level4/code-porting/python_to_cpp.py
# opens a Gradio UI; convert code and the generated C++ is written to output/<model>.cpp
```

Notes about running generated code (C++ / Java): see the Code-porting section below.

## Project structure (high level)

```
llm-engg/
├── README.md
├── pyproject.toml
├── requirements.txt
├── SETUP.md
├── .env (create this locally)
├── Level 1/
│   ├── llama/                # basic and intermediate examples (hello.py, requests examples)
│   └── tokenizer/            # tokenizer demos (tokenizer_llama.py, tokenizer_gpt.py)
├── Level2/                   # Gradio demos, multimodel, tools examples
│   ├── chat-box/
│   ├── chat-bw-llms/
│   ├── langchain/
│   └── multimodel/
├── Level3/                   # research notebooks and visualizers
└── Level4/
    └── code-porting/         # python_to_cpp.py, python_to_java.py (Gradio UI + compile/run helpers)
```

## Dependencies

See `requirements.txt` for the full list. Important ones include:

- `openai` (OpenAI-compatible client used with Ollama and cloud endpoints)
- `requests` (HTTP streaming and tokenization calls)
- `python-dotenv` (load `.env` variables)
- `transformers` (optional; used as a tokenizer fallback)
- `gradio` (UI demos)

## API endpoints (examples)

- Ollama OpenAI-compatible endpoint:

```
POST http://localhost:11434/v1/chat/completions
```

- Ollama native endpoint (tokenize / api/chat):

```
POST http://localhost:11434/api/chat
POST http://localhost:11434/api/tokenize
```

## Usage examples

1) OpenAI-compatible client (Ollama):

```python
from openai import OpenAI

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

resp = openai.chat.completions.create(
    model='llama3.2:1b',
    messages=[{"role": "user", "content": "Hello!"}],
)
print(resp.choices[0].message.content)
```

2) Ollama native (HTTP streaming and tokenize endpoints):

```python
import requests
import json

payload = {"model":"llama3.2:1b","messages":[{"role":"user","content":"Hello"}],"stream":True}
resp = requests.post('http://localhost:11434/api/chat', json=payload, stream=True)
for line in resp.iter_lines(decode_unicode=True):
    if line:
        chunk = json.loads(line)
        print(chunk.get('message', {}).get('content',''), end='')
```

## Troubleshooting

- Ollama connection errors: make sure Ollama is running and the model is available (see Quick start).
- If you see JSONDecodeError when calling the HTTP API, the server may return line-delimited JSON (streaming); parse response.iter_lines() instead of response.json().
- If a script fails with "module shadowing" (e.g., a local file named `requests.py`), rename that file — don't use filenames that match libraries you import.

Install deps if you see import errors:

```bash
pip install -r requirements.txt
# or, with uv
uv sync
```

## Code-porting (Python → C++ / Java)

Location: `Level4/code-porting/`.

- `python_to_cpp.py` — Gradio UI and helpers that:
  - send the Python snippet to a chosen model
  - write the generated C++ to `output/<safe_model>.cpp` (model id is sanitized)
  - compile & run the generated binary with `compile_and_run(<model>)` (compiles `output/<safe_model>.cpp` to `output/<safe_model>` and runs it)

- `python_to_java.py` — similar flow but targets Java 17:
  - generated Java is written to `output/Main.java`
  - compile using `javac -d output output/Main.java`
  - run with `java -cp output Main`

Notes:

- Filenames are sanitized to avoid invalid filesystem characters.
- `compile_and_run()` helpers expect the generated sources to be in the `output/` directory and give helpful error messages if compilation fails or tools are missing.

## Environment variables

Examples you may need in `.env`:

```env
GOOGLE_API_KEY=...
OPENROUTER_API_KEY=...
GROQ_API_KEY=...
HF_TOKEN=...
# Local Ollama usage with the OpenAI-compatible client uses api_key='ollama'
```

`.env` is ignored by git — never commit credentials.

## Additional resources

- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Documentation](https://python.langchain.com/)

**Last Updated**: May 24, 2026
