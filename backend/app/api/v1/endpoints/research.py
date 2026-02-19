from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging

from app.services.visibility_research import VisibilityResearchService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize service
research_service = VisibilityResearchService()


class ResearchRequest(BaseModel):
    category: str
    question_count: int = 100
    llm_engines: List[str] = ["gpt-4", "claude-3", "gemini-pro"]


class ResearchResponse(BaseModel):
    report_id: str
    category: str
    maturity: str
    brand_shares: Dict[str, float]
    cognitive_gaps: List[Dict]
    strategies: List[Dict]


@router.post("/analyze", response_model=ResearchResponse)
async def analyze_category(request: ResearchRequest):
    """
    Analyze category visibility across LLMs
    """
    try:
        logger.info(f"Analyzing category: {request.category}")
        
        result = await research_service.analyze_category(
            category=request.category,
            question_count=request.question_count,
            llm_engines=request.llm_engines
        )
        
        return ResearchResponse(**result)
        
    except Exception as e:
        logger.error(f"Research analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports")
async def list_reports():
    """
    List all visibility research reports
    """
    return {"reports": []}


@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    """
    Get specific research report
    """
    return {"report_id": report_id, "status": "completed"}
