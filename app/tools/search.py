from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from typing import List, Dict
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("Tools")

tavily_client = TavilyClient(api_key=settings.tavily_api_key)

@tool
def web_search(query: str) -> List[Dict[str, str]]:
    """Search the internet for current information on a given topic. Use this when you need up-to-date facts, news or data"""
    try:
        logger.info("LLM requested for web_search tool")
        response = tavily_client.search(query, max_results=settings.tavily_max_results)
        
        logger.info(f"web_search tool call successful")
        return [{'title': res['title'], 'url': res['url'], 'content': res['content']} for res in response['results']]
    except Exception as e:
        logger.exception(f"web_search tool call failed to retrieve the data: {str(e)}")
        return [{"Exception": f"Failed to search the query: {str(e)}"}]