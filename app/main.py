from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
from app.models.request import ResearchRequest
from app.models.response import ResearchResponse
from app.models.state import AgentState
from app.config import settings
from app.graph.workflow import agent
from rich.console import Console
from rich.markdown import Markdown
from app.utils.logger import get_logger
import tempfile
import shutil
import asyncio
import os

from app.tools.document_loader import document_loader
from app.db.vector_store import add_documents


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
    
@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    for file in files:
        _, ext = os.path.splitext(file.filename)
        if ext not in [".pdf", ".txt", ".md"]:
            return HTTPException(status_code=400, detail="Unsupported file type")
    
    temp_dir = tempfile.mkdtemp()
    file_paths = []
        
    try:
        logger.info(f"Ingesting {len(files)} files: {[f.filename for f in files]}")
       
        for file in files:
            safe_name = os.path.basename(file.filename) 
            save_path = os.path.join(temp_dir, safe_name) 
            with open(save_path, 'wb') as f:
                f.write(await file.read())
            file_paths.append(save_path)
            
        chunks = await asyncio.to_thread(document_loader, file_paths)
        logger.info(f"Created {len(chunks)} chunks from {len(files)} files")

        await asyncio.to_thread(add_documents, chunks)
        logger.info("Documents stored in vector DB")

        return {
            "files_processed": len(files),
            "total_chunks": len(chunks),
            "message": "Documents ingested successfully"
        }
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)