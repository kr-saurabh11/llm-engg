from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
import gradio as gr

load_dotenv(override=True)
GOOGLE_MODEL = "gemma-4-31b-it"
HF_MODEL = "deepseek-ai/DeepSeek-V4-Pro"
# MODEL = "gemini-3.5-flash"
# MODEL = "qwen3-coder"
db_name = "../commons/vector_db"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)

#For huggingFace llms
# hf_endpoint = HuggingFaceEndpoint(
#     repo_id=HF_MODEL,
#     temperature=0,
#     max_new_tokens=512
# )

retriever = vectorstore.as_retriever()
# print(retriever.invoke("Who is Avery?"))

# llm = ChatOpenAI(temperature=0, model_name=MODEL) # for OpenAI Models
google_llm = ChatGoogleGenerativeAI(temperature=0, model=GOOGLE_MODEL)
# hf_llm = ChatHuggingFace(llm=hf_endpoint)

print(google_llm.invoke("Who is Avery?"))
# print(hf_llm.invoke("Who is Avery?"))

SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

def answer_question(question: str, history):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    response = google_llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)])
    return response.content

answer_question("Who is Averi Lancaster?", [])

#gr.ChatInterface(answer_question).launch()


