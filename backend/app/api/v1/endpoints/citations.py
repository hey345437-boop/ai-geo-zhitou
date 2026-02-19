"""
Citation API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.services.citation_extractor import (
    CitationExtractor,
    Citation,
    CitationMetrics,
    CitationType,
    CitationCredibility
)

router = APIRouter()
citation_extractor = CitationExtractor()


class CitationResponse(BaseModel):
    """Citation response model"""
    text: str
    type: str
    url: Optional[str]
    position: str
    credibility: str
    domain: Optional[str]
    is_https: bool
    is_official: bool


class CitationMetricsResponse(BaseModel):
    """Citation metrics response"""
    total_citations: int
    citation_rate: float
    avg_credibility: float
    https_rate: float
    official_domain_rate: float
    position_distribution: dict
    credibility_distribution: dict


class ExtractCitationsRequest(BaseModel):
    """Request to extract citations"""
    response_text: str


@router.post("/extract", response_model=List[CitationResponse])
async def extract_citations(request: ExtractCitationsRequest):
    """Extract citations from LLM response text"""
    try:
        citations = citation_extractor.extract_citations(request.response_text)
        
        return [
            CitationResponse(
                text=c.text,
                type=c.type.value,
                url=c.url,
                position=c.position,
                credibility=c.credibility.name,
                domain=c.domain,
                is_https=c.is_https,
                is_official=c.is_official
            )
            for c in citations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{brand_id}", response_model=CitationMetricsResponse)
async def get_citation_metrics(
    brand_id: str,
    timeframe: str = "30d"
):
    """Get citation metrics for a brand"""
    try:
        # Mock implementation - replace with actual database query
        # In production, fetch citations from database for this brand
        
        mock_citations = [
            Citation(
                text="https://example.com/article1",
                type=CitationType.URL,
                url="https://example.com/article1",
                position="opening",
                credibility=CitationCredibility.HIGH,
                domain="example.com",
                is_https=True,
                is_official=False
            ),
            Citation(
                text="https://wikipedia.org/wiki/Brand",
                type=CitationType.URL,
                url="https://wikipedia.org/wiki/Brand",
                position="middle",
                credibility=CitationCredibility.VERY_HIGH,
                domain="wikipedia.org",
                is_https=True,
                is_official=True
            ),
        ]
        
        total_responses = 10  # Mock value
        metrics = citation_extractor.calculate_metrics(mock_citations, total_responses)
        
        return CitationMetricsResponse(
            total_citations=metrics.total_citations,
            citation_rate=metrics.citation_rate,
            avg_credibility=metrics.avg_credibility,
            https_rate=metrics.https_rate,
            official_domain_rate=metrics.official_domain_rate,
            position_distribution=metrics.position_distribution,
            credibility_distribution=metrics.credibility_distribution
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/filter")
async def filter_citations(
    brand_id: str,
    citation_type: Optional[str] = None,
    min_credibility: Optional[str] = None,
    position: Optional[str] = None
):
    """Filter citations by criteria"""
    try:
        # Mock implementation
        # In production, query database with filters
        
        return {
            "brand_id": brand_id,
            "filters": {
                "type": citation_type,
                "min_credibility": min_credibility,
                "position": position
            },
            "citations": [
                {
                    "text": "https://example.com/article",
                    "type": "url",
                    "credibility": "HIGH",
                    "position": "opening"
                }
            ],
            "total": 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
