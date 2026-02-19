from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.services.content_analyzer import content_analyzer

router = APIRouter()
logger = logging.getLogger(__name__)


class ContentAnalysisRequest(BaseModel):
    content: str
    category: str
    url: Optional[str] = None


@router.post("/analyze")
async def analyze_content(request: ContentAnalysisRequest):
    """
    Analyze content quality
    """
    try:
        logger.info(f"Analyzing content for category: {request.category}")
        
        result = content_analyzer.analyze(
            content=request.content,
            category=request.category,
            url=request.url
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Content analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
