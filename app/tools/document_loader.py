from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import os

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)


def document_loader(files: List[str]) -> List[Dict[str, Any]]:
    
    chunks = []
    
    for file in files:
        _, ext = os.path.splitext(file)
        if ext == ".pdf":
            file_loader = PyPDFLoader(file_path=file)
        elif ext == ".txt":
            file_loader = TextLoader(file_path=file)
        elif ext == ".md":
            file_loader = UnstructuredMarkdownLoader(file_path=file)
        else:
            print(f"Not a supported filed: {ext}")
            continue
            
        try:
            pages = file_loader.load()
            print(f"Document has been loaded")
        except Exception as e:
            print(f"Error loading file")
            raise
        
        chunk_data = text_splitter.split_documents(pages)
            
        chunks.extend([{'data': doc.page_content, 'metadata': doc.metadata} for doc in chunk_data])
    
    return chunks
        
        


