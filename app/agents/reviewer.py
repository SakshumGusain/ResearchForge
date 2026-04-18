from app.models.state import AgentState
from app.prompts.reviewer_prompt import REVIEWER_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from app.config import settings
from langchain_core.rate_limiters import InMemoryRateLimiter
from app.utils.logger import get_logger

logger = get_logger("Reviewer")

class ReviewResponse(BaseModel):
    status: str
    feedback: str

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.08,
    check_every_n_seconds=0.5,
    max_bucket_size=2
)

model = ChatGoogleGenerativeAI(
    model=settings.gemini_model, 
    temperature=0.0,
    google_api_key=settings.gemini_api_key,
    rate_limiter=rate_limiter    
)

structured_model = model.with_structured_output(ReviewResponse)

def reviewer_agent(state: AgentState) -> AgentState:
    draft_report = state.get('draft_report')
    if not draft_report:
        logger.debug("No draft report present for reviewer")
        raise ValueError("No draft report present for reviewer")
    
    research_data = state.get('research_data', [])
    research_content = "\n\n".join([str(msg.content) for msg in research_data])
    analysis = state.get('analysis')
    
    content = (
        f"Topic: \n{state.get('topic')}\n\n"
        f"Draft Report: \n{draft_report}\n\n"
        f"Analysis: \n{analysis}\n\n"
        f"Research Source: \n{research_content}"
    )
    
    response = structured_model.invoke([REVIEWER_PROMPT, HumanMessage(content=content)])
    
    if response.status == "APPROVED":
        state['review_feedback'] = response.feedback
        state['final_report'] = draft_report
        state['status'] = "approved"
        logger.info(f"Status: APPROVED (iteration: {state.get('iteration_count')})")
        logger.info("Final report ready")
    else:
        state['review_feedback'] = response.feedback
        state['iteration_count'] = state.get('iteration_count', 0) + 1
        logger.info(f"Status: NEEDS REVISION (iteration: {state.get('iteration_count')})")
    
    return state
        

    