import os
import asyncio
from dotenv import load_dotenv

# Path to the .env file in the root
load_dotenv(dotenv_path="../.env")

# Adjust sys.path to import from current project structure
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.openai_service import extract_resume_details, generate_career_paths
from app.services.chroma_service import add_resume_to_vector_store, query_resume_context

async def test_llm():
    print("Testing Gemini LLM...")
    try:
        sample_text = "I am a software engineer with 5 years of experience in Python and React."
        response = await extract_resume_details(sample_text)
        print("LLM Response:")
        print(response)
    except Exception as e:
        print(f"LLM Test Failed: {e}")

async def test_embeddings():
    print("\nTesting Gemini Embeddings and ChromaDB...")
    try:
        user_id = "test_user_123"
        resume_id = "test_resume_456"
        resume_text = "Experienced Data Scientist with expertise in Machine Learning and Deep Learning."
        
        # Test adding
        print("Adding resume to vector store...")
        add_resume_to_vector_store(resume_text, user_id, resume_id)
        
        # Test querying
        print("Querying vector store...")
        results = query_resume_context("Who is a data scientist?", user_id)
        print(f"Query Results: {results}")
    except Exception as e:
        print(f"Embeddings Test Failed: {e}")

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "YOUR_GEMINI_API_KEY_HERE":
        print("ERROR: Please set a valid GOOGLE_API_KEY in the .env file before running this test.")
    else:
        asyncio.run(test_llm())
        asyncio.run(test_embeddings())
