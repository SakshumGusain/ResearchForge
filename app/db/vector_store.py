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
    
    # Filter out empty/whitespace-only chunks
    valid_chunks = [chunk for chunk in chunks if chunk['data'].strip()]
    if not valid_chunks:
        return
    
    texts = [chunk['data'] for chunk in valid_chunks]
    metadatas = [chunk['metadata'] for chunk in valid_chunks]
    
    ids = [hashlib.md5(f"{text}_{i}".encode()).hexdigest() for i, text in enumerate(texts)]
    
    # Deduplicate before embedding to avoid wasted API calls
    seen = {}
    unique_ids, unique_texts, unique_metadatas = [], [], []
    for idx, doc_id in enumerate(ids):
        if doc_id not in seen:
            seen[doc_id] = True
            unique_ids.append(doc_id)
            unique_texts.append(texts[idx])
            unique_metadatas.append(metadatas[idx])
    
    all_embeddings = [embedding_model.embed_query(text) for text in unique_texts]
    
    if len(all_embeddings) != len(unique_ids):
        raise ValueError(
            f"Embedding count mismatch: got {len(all_embeddings)} embeddings for {len(unique_ids)} documents. "
            f"Check if the embedding model '{settings.gemini_embedding_model}' supports batch embedding."
        )

    collection.add(ids=unique_ids, embeddings=all_embeddings, documents=unique_texts, metadatas=unique_metadatas)

def similarity_search(query, k=5):
    """Takes a query string converts that into embedding and find k most similar document chunks, and returns them"""
    
    query_embeddings = embedding_model.embed_query(query)
    result = collection.query(query_embeddings=[query_embeddings], n_results=k)
    
    return result['documents'][0] # returns list of text chunks