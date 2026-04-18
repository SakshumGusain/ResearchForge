from app.models.state import AgentState
from app.tools.rag import knowledge_base_search
from app.tools.search import web_search
from langchain_google_genai import ChatGoogleGenerativeAI
from app.prompts.researcher_prompt import RESEARCHER_PROMPT
from langchain_core.messages import HumanMessage
from app.config import settings
from langchain_core.rate_limiters import InMemoryRateLimiter
from app.utils.logger import get_logger

logger = get_logger("Researcher")

tools = [knowledge_base_search, web_search]

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.08,
    check_every_n_seconds=0.5,
    max_bucket_size=2
)

model = ChatGoogleGenerativeAI(
    model=settings.gemini_model, 
    temperature=0.3, 
    google_api_key=settings.gemini_api_key,
    rate_limiter=rate_limiter
).bind_tools(tools)



def research_agent(state: AgentState) -> AgentState:
    """function that uses web search tool and RAG tool for internal docs, and combines the results into structured findings"""
    if not state.get('topic'):
        logger.debug("Topic to perform research not found")
        raise ValueError("Topic not found to perform research operations")
    
    logger.info(f"Starting research on topic: {state.get('topic')}")
    
    query = HumanMessage(content=state.get('topic'))
    messages = state.get('messages', [])
    tool_results = [msg for msg in messages if getattr(msg, 'type', '') == 'tool']
    if tool_results:
        state['research_data'].extend(tool_results)

    response = model.invoke([RESEARCHER_PROMPT, query])
    
    if response.tool_calls:
        logger.debug(f"LLM response has {len(response.tool_calls)} tool calls")
    else:
        logger.info(f"Research complete. Total data points: {len(state.get('research_data'))}")
    
    state['research_data'].append(response)
    state['messages'] = [response]
    
    return state

def should_research_continue(state: AgentState):
    research_data = state.get('research_data')
    if not research_data:
        return "tools"

    last_data = research_data[-1]
    
    if len(research_data) > 2:
        return "supervisor"
    
    if not last_data.tool_calls:
        logger.debug(f"Research continue check: {len(research_data)} data points, routing to supervisor")
        return "supervisor"
    else:
        logger.debug(f"Research continue check: {len(research_data)} data points, routing to tools")
        return "tools"
    