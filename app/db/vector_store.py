import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import hashlib
from typing import List, Dict, Any
from app.config import settings

client = chromadb.PersistentClient(settings.chroma_persist_dir)
collection = client.get_or_create_collection(name=settings.chroma_collection_name)
embedding_model = GoogleGenerativeAIEmbeddings(model=settings.gemini_embedding_model, api_key=settings.gemini_api_key)

def add_documents(chunks: List[Dict[str, Any]]):
    """Takes a list of text chunks and store them with their embeddings"""
    
    texts = [chunk['data'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]
    
    embeddings = embedding_model.embed_documents(texts)
    ids = [hashlib.md5(text.encode()).hexdigest() for text in texts]
    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)


def similarity_search(query, k=5):
    """Takes a query string converts that into embedding and find k most similar document chunks, and returns them"""
    
    query_embeddings = embedding_model.embed_query(query)
    result = collection.query(query_embeddings=[query_embeddings], n_results=k)
    
    return result['documents'][0] # returns list of text chunks