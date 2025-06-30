import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

VECTORSTORE_PATH = "vectorstore"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "mistralai/mistral-7b-instruct"
