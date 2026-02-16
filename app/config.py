import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Config
    APP_NAME = "Multi-Agent Support System"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # LLM Config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    
    # RAG Config
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_RETRIEVED_DOCS = 3
    
    # AWS Config
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    
settings = Settings()