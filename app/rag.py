import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List

class RAGRetriever:
    """
    Retrieval-Augmented Generation system using FAISS and Sentence Transformers
    """
    
    def __init__(self, docs: List[str], embedding_model: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.docs = docs
        self.embeddings = self.model.encode(docs)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype(np.float32))
    
    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve top-k relevant documents for a query"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype(np.float32), 
            top_k
        )
        return [self.docs[i] for i in indices[0] if i < len(self.docs)]
    
    def load_docs_from_file(self, filepath: str):
        """Load documents from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        # Handle both array and object with 'documents' key
        if isinstance(data, list):
            self.docs = [doc.get('content', '') for doc in data]
        else:
            self.docs = [doc.get('content', '') for doc in data.get('documents', [])]
        
        self.embeddings = self.model.encode(self.docs)
        
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype(np.float32))

# Initialize global retriever
def init_retriever(docs: List[str] = None) -> RAGRetriever:
    """Factory function to initialize RAG retriever"""
    if docs is None:
        # Try to load from file first
        try:
            import os
            docs_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'docs.json')
            if os.path.exists(docs_path):
                retriever = RAGRetriever([])
                retriever.load_docs_from_file(docs_path)
                return retriever
        except Exception as e:
            print(f"Warning: Could not load docs from file: {e}")
        
        # Fallback to default docs
        docs = [
            "To reset your password, go to login page and click 'Forgot Password'",
            "For billing questions, contact billing@support.com or visit billing portal",
            "Technical support available 24/7 at support@example.com",
            "Account settings can be changed in the user dashboard",
            "For urgent issues, call our support hotline: 1-800-SUPPORT"
        ]
    return RAGRetriever(docs)