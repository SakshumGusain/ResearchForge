from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    research_data: list
    analysis: str
    draft_report: any
    review_feedback: any
    final_report: any
    current_agent: any
    iteration_count: int
    status: str