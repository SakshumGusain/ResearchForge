from app.models.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from app.prompts.analyst_prompt import ANALYST_PROMPT
from langchain_core.messages import HumanMessage
from app.config import settings
from langchain_core.rate_limiters import InMemoryRateLimiter
from app.utils.logger import get_logger

logger = get_logger("Analyst")

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
)


def analyst_agent(state: AgentState) -> AgentState:
    """agent which takes raw research message and convert that raw message to structured analysis by including key insights, gaps, contradictions etc"""
    
    research_data = state.get('research_data')
    if not research_data:
        logger.debug("No research data available to analyse")
        raise ValueError("No research data available to analyse")
    
    logger.info(f"Analysing research data ({len(research_data)} sources)")
    research_content = "\n\n".join([str(msg.content) for msg in research_data])
    response = model.invoke([ANALYST_PROMPT, HumanMessage(content=f"Topic: {state.get('topic')}\n\nResearch Data: \n{research_content}")])
    
    state['analysis'] = response.content
    logger.info(f"Analysis complete ({len(response.content)} chars)")
    
    return state
    