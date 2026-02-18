import google.generativeai as genai
import chromadb
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Always resolve to project_root/data/chroma_db regardless of working directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # backend/app/services -> root
CHROMA_DB_PATH = str(PROJECT_ROOT / "data" / "chroma_db")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Use Google Gemini Embeddings - direct SDK implementation
class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name="models/gemini-embedding-001"):
        self.model_name = model_name
    def __call__(self, input):
        # input is a list of strings
        if isinstance(input, str):
            input = [input]
        response = genai.embed_content(model=self.model_name, content=input)
        return response['embedding']
    def embed_query(self, text=None, **kwargs):
        # Handle case where Chroma calls with 'input' keyword
        content = text if text is not None else kwargs.get("input")
        if content is None:
            raise ValueError("No text provided for embedding query")
        response = genai.embed_content(model=self.model_name, content=content)
        return response['embedding']
    def name(self):
        return "gemini_embeddings"

chroma_gemini_ef = GeminiEmbeddingFunction()

resume_collection = client.get_or_create_collection(name="resume_embeddings_v4", embedding_function=chroma_gemini_ef)
chat_collection = client.get_or_create_collection(name="chat_history_embeddings_v4", embedding_function=chroma_gemini_ef)

def add_resume_to_vector_store(resume_text: str, user_id: str, resume_id: str):
    resume_collection.add(
        documents=[resume_text],
        metadatas=[{"user_id": user_id, "resume_id": resume_id}],
        ids=[resume_id]
    )

def query_resume_context(query_text: str, user_id: str, resume_id: str = None, n_results: int = 2):
    where_filter = {"user_id": user_id}
    if resume_id:
        where_filter = {
            "$and": [
                {"user_id": user_id},
                {"resume_id": str(resume_id)}
            ]
        }
        
    results = resume_collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where_filter
    )
    return results['documents'][0] if results['documents'] else []

def add_chat_to_vector_store(chat_text: str, user_id: str, session_id: str, message_id: str):
    chat_collection.add(
        documents=[chat_text],
        metadatas=[{"user_id": user_id, "session_id": session_id}],
        ids=[message_id]
    )

def query_chat_history(query_text: str, session_id: str, n_results: int = 5):
    results = chat_collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"session_id": session_id}
    )
    return results['documents'][0] if results['documents'] else []

def query_user_chat_history(query_text: str, user_id: str, n_results: int = 10):
    """Query chat history across ALL sessions for a user — gives cross-session awareness."""
    results = chat_collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"user_id": user_id}
    )
    return results['documents'][0] if results['documents'] else []
