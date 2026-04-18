from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum

class Scan(Enum):
    quick = 'quick'
    detailed = 'detailed'

class ResearchRequest(BaseModel):
    topic: Annotated[str, Field(..., description="Request message from user")]
    max_sources: Annotated[int, Field(..., ge=0, description="Maximum number of sources that can be used")]
    depth: Annotated[Scan, Field(..., description="Scanning technique can be 'quick' or 'detailed'")]