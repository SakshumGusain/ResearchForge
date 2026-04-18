from app.models.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.prompts.writer_prompt import WRITER_INITIAL_PROMPT, WRITER_FEEDBACK_PROMPT
from app.config import settings
from langchain_core.rate_limiters import InMemoryRateLimiter
from app.utils.logger import get_logger

logger = get_logger("Writer")

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.08,
    check_every_n_seconds=0.5,
    max_bucket_size=2
)

model = ChatGoogleGenerativeAI(
    model=settings.gemini_model, 
    temperature=0.7, 
    google_api_key=settings.gemini_api_key,
    rate_limiter=rate_limiter
)

def writer_agent(state: AgentState) -> AgentState:
    """takes the analysis raw report and convert that into well structured, readable report"""
    analysis = state.get('analysis')
    if not analysis:
        logger.debug("Analysis not present to draft the report")
        raise ValueError("Analysis not present to draft the report")
    
    research_data = state.get('research_data')
    research_content = "\n\n".join([str(msg.content) for msg in research_data])

    review_feedback = state.get('review_feedback')

    if not review_feedback:
        logger.info("Writing first draft")
        content = f"Topic: \n{state.get('topic')}\n\nAnalysis: \n{analysis}\n\nResearch Source: \n{research_content}"
        response = model.invoke([WRITER_INITIAL_PROMPT, HumanMessage(content=content)])
    else:
        logger.info(f"Writing {state.get('iteration_count')} draft, after reviewing feedback")
        content = f"Topic: \n{state.get('topic')}\n\nAnalysis: \n{analysis}\n\nPrevious Draft: \n{state.get('draft_report')}\n\nReviewer Feedback: \n{review_feedback}\n\nResearch Source: \n{research_content}"
        response = model.invoke([WRITER_FEEDBACK_PROMPT, HumanMessage(content=content)])
        
    state['draft_report'] = response.content
    logger.info(f"Draft complete ({len(response.content)} chars)")
        
    return state