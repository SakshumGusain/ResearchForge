from fastapi import FastAPI
from app.models.request import ResearchRequest
from app.models.response import ResearchResponse
from app.models.state import AgentState
from app.config import settings
from app.graph.workflow import agent
from rich.console import Console
from rich.markdown import Markdown
from app.utils.logger import get_logger

logger = get_logger("Request")

app = FastAPI()
console = Console()

@app.get("/health")
def health():
    logger.info("FastAPI server is up and running")
    return {'message': 'api is working'}

@app.post("/research")
def research(request: ResearchRequest):
    
    logger.info(f"Received research request: topic={request.topic}, depth={request.depth}")
    
    state = AgentState(topic=request.topic, messages=[], research_data=[], analysis="", draft_report="", review_feedback={}, final_report="", current_agent="", iteration_count=0, status="")
    
    response = agent.invoke(state)
    
    logger.info("Final report is generated successfully")
    print("="*60 + "\n")
    console.print(Markdown(response["final_report"]))
    print("="*60 + "\n")
    
    logger.info(f"Research complete. Report: {len(response['final_report'])} chars, Iterations: {state.get('iteration_count')}")
    return {'response': response}
    