from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import logging
import random

router = APIRouter()
logger = logging.getLogger(__name__)


class OptimizationRequest(BaseModel):
    brand_id: str
    current_visibility: float
    competitor_data: Dict[str, float]


@router.post("/recommend")
async def get_recommendations(request: OptimizationRequest):
    """
    Get optimization recommendations based on current performance
    """
    try:
        logger.info(f"Generating recommendations for brand: {request.brand_id}")
        
        recommendations = []
        
        # Analyze competitive position
        avg_competitor_visibility = sum(request.competitor_data.values()) / len(request.competitor_data)
        visibility_gap = avg_competitor_visibility - request.current_visibility
        
        if visibility_gap > 0.1:
            recommendations.append({
                "type": "competitive_gap",
                "priority": "high",
                "title": "Close Competitive Gap",
                "description": f"Your visibility is {visibility_gap:.1%} below average competitor",
                "action": "Focus on high-impact content improvements and citation building",
                "expected_impact": min(visibility_gap * 0.7, 0.30)
            })
        
        # Content quality recommendations
        if request.current_visibility < 0.7:
            recommendations.append({
                "type": "content_quality",
                "priority": "high",
                "title": "Improve Content Quality",
                "description": "Content quality scores indicate room for improvement",
                "action": "Add more authoritative sources, data, and expert opinions",
                "expected_impact": 0.20
            })
        
        # Citation recommendations
        recommendations.append({
            "type": "citations",
            "priority": "medium",
            "title": "Build Citation Network",
            "description": "Increase credible citations to boost authority",
            "action": "Get featured in industry publications and authoritative sources",
            "expected_impact": 0.15
        })
        
        # Freshness recommendations
        recommendations.append({
            "type": "freshness",
            "priority": "medium",
            "title": "Update Content Regularly",
            "description": "Keep content fresh with latest information",
            "action": "Add recent data, trends, and time-sensitive information",
            "expected_impact": 0.12
        })
        
        # Entity coverage
        recommendations.append({
            "type": "entity_coverage",
            "priority": "low",
            "title": "Expand Entity Coverage",
            "description": "Mention more relevant entities and concepts",
            "action": "Include related brands, products, locations, and industry terms",
            "expected_impact": 0.08
        })
        
        # Sort by priority and impact
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(
            key=lambda r: (priority_order[r["priority"]], -r["expected_impact"])
        )
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        logger.error(f"Failed to generate recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies")
async def get_strategies():
    """Get available GEO strategies"""
    return {
        "strategies": [
            {
                "id": "content_optimization",
                "name": "Content Optimization",
                "description": "Improve content quality and relevance",
                "tactics": ["keyword_density", "entity_coverage", "structure"]
            },
            {
                "id": "authority_building",
                "name": "Authority Building",
                "description": "Build credibility and trust signals",
                "tactics": ["citations", "expert_quotes", "data_sources"]
            },
            {
                "id": "freshness_maintenance",
                "name": "Freshness Maintenance",
                "description": "Keep content up-to-date",
                "tactics": ["regular_updates", "trending_topics", "recent_data"]
            }
        ]
    }
