from app.models.state import AgentState
from langgraph.graph import END
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("Supervisor")

def supervisor_agent(state: AgentState):
    """Router agent which will route to a agent based on Research, Analysis, Writer and Reviewer"""


    if not state.get('research_data'):
        logger.info("Routing to: Researcher(reason: no research data)")
        return 'researcher'
    elif not state.get('analysis'):
        logger.info("Routing to: Analyst(reason: research done, no analysis)")
        return 'analyst'
    elif not state.get('draft_report'):
        logger.info("Routing to: Writer(reason: analysis done, no draft)")
        return 'writer'
    elif not state.get('review_feedback'):
        logger.info("Routing to: Reviewer(reason: draft exists, no review)")
        return 'reviewer'
    elif state.get('status') == "approved":
        logger.info("Routing to: END(reason: approved)")
        return END
    elif state.get('iteration_count') < settings.max_revision_iterations:
        logger.info(f"Routing to: Writer(reason: revision needed, iteration {state.get('iteration_count')}/{settings.max_revision_iterations})")
        return 'writer'
    else:
        logger.info(f"Routing to: END")
        return END