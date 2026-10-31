from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from commons.response_sanitizer import sanitize_response
from dotenv import load_dotenv



load_dotenv(override=True)

HF_MODEL = "deepseek-ai/DeepSeek-V4-Pro"
GOOGLE_MODEL = "gemma-4-31b-it"
# GOOGLE_MODEL = "gemini-2.5-flash"
DB_NAME = str(Path(__file__).parent.parent.parent / "commons/vector_db")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
RETRIEVAL_K = 10

SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever()
hf_endpoint = HuggingFaceEndpoint(
    repo_id=HF_MODEL,
    temperature=0,
    max_new_tokens=512
)

# llm = ChatOpenAI(temperature=0, model_name=MODEL)
google_llm = ChatGoogleGenerativeAI(temperature=0, model=GOOGLE_MODEL)
# hf_llm = ChatHuggingFace(llm=hf_endpoint)


def fetch_context(question: str) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    return retriever.invoke(question, k=RETRIEVAL_K)


def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    print("Combined question: ", prior + "\n" + question)
    return prior + "\n" + question


def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document]]:
    """
    Answer the given question with RAG; return the answer and the context documents.
    """
    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    #print(f"Messages->:{messages}")
    response = google_llm.invoke(messages)
    # print(f"Response->:{response.content}")
    # return response.content, docs
    return sanitize_response(response.content), docs
