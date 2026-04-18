from langchain.tools import tool
from app.db.vector_store import similarity_search
from typing import List, Dict, Any
from app.utils.logger import get_logger

logger = get_logger("Tools")

@tool
def knowledge_base_search(query: str) -> List[Dict[str, Any]]:
    """Search the internal document knowledge base for information. Use this when you need to find information from internal reports, papers, or documents that have been previously ingested"""
    try:
        logger.info("LLM requested for knowledge_base_search tool")
        result = similarity_search(query, k=5)
        if not result:
            logger.info("No data found in knowledge_base_search tool call")
            return []
        
        logger.info("knowledge_base_search tool call successfull")
        return [{'source': 'internal_kb', 'title': query, 'content': str(doc)} for i, doc in enumerate(result)]
    except Exception as e:
        logger.exception(f"Failed to search the query from internal knowledge base: {str(e)}")
        return [{"Exception": f"Failed to search the query from internal knowledge base: {str(e)}"}]
    
    