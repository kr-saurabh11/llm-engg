import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import subprocess
from my_system_info import retrieve_system_info
import re

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
hf_token = os.getenv('HF_TOKEN')

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
    print("Groq API Key not set (and this is optional)")

if openrouter_api_key:
    print(f"OpenRouter API Key exists and begins {openrouter_api_key[:6]}")
else:
    print("OpenRouter API Key not set (and this is optional)")

if hf_token:
    print(f"HF_TOKEN exists and begins {hf_token[:2]}")
else:
    print("HF_TOKEN not set (and this is optional)")

# Connect to client libraries

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
groq_url = "https://api.groq.com/openai/v1"
ollama_url = "http://localhost:11434/v1"
openrouter_url = "https://openrouter.ai/api/v1"
huggingface_url = "https://router.huggingface.co/v1"

gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)
groq = OpenAI(api_key=groq_api_key, base_url=groq_url)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)
openrouter = OpenAI(api_key=openrouter_api_key, base_url=openrouter_url)
huggingface = OpenAI(api_key=hf_token, base_url=huggingface_url)

models = ["gemini-3.5-flash", "gemini-2.5-flash", "gemma-4-31b-it", "deepseek-ai/DeepSeek-V4-Pro",
          "deepseek-ai/DeepSeek-V4-Flash", "Qwen/Qwen2.5-Coder-3B-Instruct:nscale", "Qwen/Qwen3.5-397B-A17B:scaleway",
          "meta-llama/Llama-3.3-70B-Instruct", "openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3-32b",
          "llama3.2:1b", "baidu/cobuddy:free","qwen/qwen3-coder:free"]

clients = {"gemini-3.5-flash": gemini, "gemini-2.5-flash": gemini, "gemma-4-31b-it": gemini,
           "deepseek-ai/DeepSeek-V4-Pro": huggingface, "deepseek-ai/DeepSeek-V4-Flash": huggingface,
           "Qwen/Qwen2.5-Coder-3B-Instruct:nscale": huggingface, "Qwen/Qwen3.5-397B-A17B:scaleway": huggingface,
           "meta-llama/Llama-3.3-70B-Instruct": huggingface, "openai/gpt-oss-20b": groq, "openai/gpt-oss-120b": groq,
           "qwen/qwen3-32b": groq, "llama3.2:1b": ollama,
           "baidu/cobuddy:free": openrouter, "qwen/qwen3-coder:free": openrouter}
system_info = retrieve_system_info()

system_prompt = """
Your task is to convert Python code into high performance C++ code.
Respond only with C++ code. Do not provide any explanation other than occasional comments.
The C++ response needs to produce an identical output in the fastest possible time.
"""

def build_compile_command(file):
    # `file` is the base name (without extension) located in the `output` directory
    output_dir = "output"
    src = os.path.join(output_dir, f"{file}.cpp")
    out = os.path.join(output_dir, file)
    compile_command = [
        "clang++",
        "-std=c++17",
        "-Ofast",
        "-mcpu=native",
        "-flto=thin",
        "-fvisibility=hidden",
        "-DNDEBUG",
        src,
        "-o",
        out,
    ]
    return compile_command

def build_run_command(file):
    # `file` is the base name (without extension) located in the `output` directory
    out = os.path.join("output", file)
    run_command = [out]
    return run_command

def user_prompt_for(python):
    return f"""
Port this Python code to C++ with the fastest possible implementation that produces identical output in the least time.
The system information is:
{system_info}
Your response will be written to a file called main.cpp and then compiled and executed; the compilation command is:
{build_compile_command("main")}
Respond only with C++ code. No explanation other than occasional comments.
Python code to port:

```python
{python}
```
"""


def messages_for(python):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(python)}
    ]

def write_output(model, cpp):
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    # sanitize model name to create a safe filename
    safe_model = re.sub(r"[^A-Za-z0-9_.-]", "_", model)
    file_path = os.path.join(
        output_dir,
        f"{safe_model}.cpp"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cpp)

    return file_path

def port(model, python):
    try:
        client = clients.get(model)
        if client is None:
            return f"Error: No client configured for model '{model}'. Please set the required API key or choose a different model."

        reasoning_effort = "high" if 'gpt' in model else None
        response = client.chat.completions.create(
            model=model,
            messages=messages_for(python),
            reasoning_effort=reasoning_effort,
        )

        reply = response.choices[0].message.content
        reply = reply.replace('```cpp', '').replace('```', '')
        write_output(model, reply)
        return reply
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"[port] Exception while converting with model {model}: {e}\n{tb}")
        return f"Error: {type(e).__name__}: {e}\nSee server logs for traceback."

pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(200_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
"""

def run_python(code):
    globals_dict = {"__builtins__": __builtins__}

    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        exec(code, globals_dict)
        output = buffer.getvalue()
    except Exception as e:
        output = f"Error: {e}"
    finally:
        sys.stdout = old_stdout

    return output

def compile_and_run(model="main"):
    """Compile and run the generated C++ file from the `output` directory.

    model: base filename (without extension) stored under `output/<model>.cpp`.
    """
    try:
        # sanitize model name to match the filename written by write_output()
        safe_model = re.sub(r"[^A-Za-z0-9_.-]", "_", model)
        compile_cmd = build_compile_command(safe_model)
        subprocess.run(compile_cmd, check=True, text=True, capture_output=True)
        print("Compilation successful!\n")

        # Run the compiled binary 3 times
        for i in range(3):
            result = subprocess.run(build_run_command(safe_model), check=True, text=True, capture_output=True, timeout=30)
            print(f"Run {i+1} output:\n{result.stdout}")

    except subprocess.CalledProcessError as e:
        stderr = e.stderr if hasattr(e, 'stderr') and e.stderr else str(e)
        print(f"Compilation/Run error:\n{stderr}")
    except FileNotFoundError:
        print(f"Error: Compiler or binary not found. Ensure 'clang++' is installed and the source file exists in the 'output' directory.")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")

with gr.Blocks() as ui:
    with gr.Row():
        python = gr.Textbox(label="Python code:", lines=28, value=pi)
        cpp = gr.Textbox(label="C++ code:", lines=28)
    with gr.Row():
        model = gr.Dropdown(models, label="Select model", value=models[0])
        convert = gr.Button("Convert code")

    convert.click(port, inputs=[model, python], outputs=[cpp])

#ui.launch(inbrowser=True,theme=gr.themes.Citrus())

py_output = run_python(pi)
print(py_output)
print("---"*50)
compile_and_run("gemini-2.5-flash")
print("---"*50)
compile_and_run("gemini-3.5-flash")



