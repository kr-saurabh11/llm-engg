# Setup Guide

Follow the steps below to set up the project locally.

## Install Ollama (Run LLM Locally)
### Download and install Ollama:
`curl -fsSL https://ollama.com/install.sh | sh`

### Verify installation:
`ollama --version`

## Run the LLM Model
### Start the LLM locally using:

`ollama run llama3.2:1b`

This will download (if not already) and run the model.

## Install uv (Python Package Manager)
### Download and install uv:
`curl -LsSf https://astral.sh/uv/install.sh | sh`

### Verify uv Installation
`uv --version`

## Initialize Project
### From the project directory, run:

`uv init`
`uv sync`
