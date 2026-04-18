from pydantic import BaseModel, Field
from typing import List, Dict, Annotated, Any

class ResearchResponse(BaseModel):
    report: Annotated[str, Field(..., description="Response for the user's request")]
    sources: Annotated[List[str], Field(..., description="List of sources used to generate the report")]
    metadata: Dict[str, Any]