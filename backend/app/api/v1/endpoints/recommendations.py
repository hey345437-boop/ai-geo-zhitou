"""
Optimization & Recommendations API Endpoints

Provides endpoints for generating optimization recommendations and compliance checking.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.services.optimization_engine import (
    RecommendationGenerator,
    ComplianceChecker,
    RecommendationType,
    RecommendationPriority
)

router = APIRouter()
recommendation_generator = RecommendationGenerator()
compliance_checker = ComplianceChecker()


# Request/Response Models
class GenerateRecommendationsRequest(BaseModel):
    """Request model for generating recommendations"""
    project_id: str
    content_analysis: Dict[str, Any] = Field(..., description="Content analysis results")
    visibility_score: float = Field(..., ge=0, le=100)
    competitive_data: Optional[Dict[str, Any]] = None


class ApplyRecommendationRequest(BaseModel):
    """Request model for applying recommendation"""
    applied: bool = Field(True, description="Whether recommendation was applied")
    notes: Optional[str] = None


class ComplianceCheckRequest(BaseModel):
    """Request model for compliance check"""
    content_id: str
    content: str = Field(..., description="Plain text content")
    html: Optional[str] = Field(None, description="HTML content")


class RecommendationResponse(BaseModel):
    """Response model for recommendation"""
    recommendation_id: str
    type: str
    priority: str
    title: str
    description: str
    action: str
    expected_impact: float
    effort_level: str
    code_example: Optional[str]
    is_white_hat: bool
    compliance_notes: Optional[str]
    created_at: str


class ComplianceReportResponse(BaseModel):
    """Response model for compliance report"""
    content_id: str
    compliance_score: float
    is_compliant: bool
    issues_count: int
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    checked_at: str


@router.post("/recommendations/generate", response_model=List[RecommendationResponse])
async def generate_recommendations(request: GenerateRecommendationsRequest):
    """
    Generate optimization recommendations
    
    Analyzes content and generates prioritized recommendations for
    improving LLM visibility.
    """
    try:
        recommendations = recommendation_generator.generate_recommendations(
            project_id=request.project_id,
            content_analysis=request.content_analysis,
            visibility_score=request.visibility_score,
            competitive_data=request.competitive_data
        )
        
        return [
            RecommendationResponse(
                recommendation_id=rec.recommendation_id,
                type=rec.type.value,
                priority=rec.priority.value,
                title=rec.title,
                description=rec.description,
                action=rec.action,
                expected_impact=rec.expected_impact,
                effort_level=rec.effort_level,
                code_example=rec.code_example,
                is_white_hat=rec.is_white_hat,
                compliance_notes=rec.compliance_notes,
                created_at=rec.created_at.isoformat()
            )
            for rec in recommendations
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/recommendations/{project_id}", response_model=List[RecommendationResponse])
async def get_recommendations(
    project_id: str,
    priority: Optional[str] = Query(None, description="Filter by priority"),
    type: Optional[str] = Query(None, description="Filter by type")
):
    """
    Get recommendations for a project
    
    Retrieves previously generated recommendations with optional filtering.
    """
    recommendations = recommendation_generator.recommendations.get(project_id, [])
    
    # Apply filters
    if priority:
        try:
            priority_enum = RecommendationPriority(priority)
            recommendations = [r for r in recommendations if r.priority == priority_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")
    
    if type:
        try:
            type_enum = RecommendationType(type)
            recommendations = [r for r in recommendations if r.type == type_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid type: {type}")
    
    return [
        RecommendationResponse(
            recommendation_id=rec.recommendation_id,
            type=rec.type.value,
            priority=rec.priority.value,
            title=rec.title,
            description=rec.description,
            action=rec.action,
            expected_impact=rec.expected_impact,
            effort_level=rec.effort_level,
            code_example=rec.code_example,
            is_white_hat=rec.is_white_hat,
            compliance_notes=rec.compliance_notes,
            created_at=rec.created_at.isoformat()
        )
        for rec in recommendations
    ]


@router.post("/recommendations/{recommendation_id}/apply")
async def apply_recommendation(
    recommendation_id: str,
    request: ApplyRecommendationRequest
):
    """
    Mark recommendation as applied
    
    Records that a recommendation has been implemented.
    """
    # In production, update database
    return {
        'recommendation_id': recommendation_id,
        'applied': request.applied,
        'applied_at': '2026-02-12T00:00:00Z',
        'notes': request.notes
    }


@router.get("/recommendations/types")
async def get_recommendation_types():
    """
    Get available recommendation types
    
    Returns all available recommendation types and their descriptions.
    """
    return {
        'types': [
            {
                'value': t.value,
                'name': t.name,
                'description': {
                    'content_quality': 'Improve content relevance and depth',
                    'schema_markup': 'Add structured data markup',
                    'citation_improvement': 'Enhance authority with citations',
                    'structure_fix': 'Fix content structure issues',
                    'keyword_optimization': 'Optimize keyword usage',
                    'entity_enhancement': 'Add more named entities',
                    'compliance_fix': 'Fix compliance violations'
                }.get(t.value, '')
            }
            for t in RecommendationType
        ]
    }


@router.post("/compliance/check", response_model=ComplianceReportResponse)
async def check_compliance(request: ComplianceCheckRequest):
    """
    Check content compliance
    
    Analyzes content for compliance with white-hat SEO practices and
    detects potential violations.
    """
    try:
        report = compliance_checker.check_compliance(
            content_id=request.content_id,
            content=request.content,
            html=request.html
        )
        
        return ComplianceReportResponse(
            content_id=report.content_id,
            compliance_score=report.compliance_score,
            is_compliant=report.is_compliant,
            issues_count=len(report.issues),
            issues=[issue.to_dict() for issue in report.issues],
            recommendations=report.recommendations,
            checked_at=report.checked_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check compliance: {str(e)}"
        )


@router.get("/compliance/{content_id}")
async def get_compliance_report(content_id: str):
    """
    Get compliance report for content
    
    Retrieves the most recent compliance report for the specified content.
    """
    # In production, fetch from database
    # For now, return mock data
    return {
        'content_id': content_id,
        'compliance_score': 85.0,
        'is_compliant': True,
        'last_checked': '2026-02-12T00:00:00Z',
        'issues_count': 2
    }


@router.get("/optimization/schema/generate")
async def generate_schema(
    content_type: str = Query(..., description="Content type (article, product, etc.)"),
    data: str = Query(..., description="JSON data for schema")
):
    """
    Generate Schema.org markup
    
    Creates appropriate Schema.org JSON-LD markup based on content type.
    """
    import json
    
    try:
        content_data = json.loads(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    
    # Generate schema based on type
    if content_type == 'article':
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": content_data.get('title', ''),
            "author": {
                "@type": "Person",
                "name": content_data.get('author', '')
            },
            "datePublished": content_data.get('date', ''),
            "description": content_data.get('description', '')
        }
    elif content_type == 'product':
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": content_data.get('name', ''),
            "description": content_data.get('description', ''),
            "offers": {
                "@type": "Offer",
                "price": content_data.get('price', ''),
                "priceCurrency": content_data.get('currency', 'USD')
            }
        }
    elif content_type == 'local_business':
        schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": content_data.get('name', ''),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": content_data.get('street', ''),
                "addressLocality": content_data.get('city', ''),
                "addressRegion": content_data.get('state', ''),
                "postalCode": content_data.get('zip', '')
            },
            "telephone": content_data.get('phone', '')
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported content type: {content_type}")
    
    return {
        'content_type': content_type,
        'schema': schema,
        'json_ld': json.dumps(schema, indent=2)
    }


@router.get("/optimization/best-practices")
async def get_best_practices(
    category: Optional[str] = Query(None, description="Category (content, technical, etc.)")
):
    """
    Get optimization best practices
    
    Returns best practices for improving LLM visibility.
    """
    best_practices = {
        'content': [
            "Write comprehensive, in-depth content",
            "Answer user questions directly",
            "Use clear, concise language",
            "Include relevant examples and data",
            "Update content regularly"
        ],
        'technical': [
            "Add Schema.org structured data",
            "Use proper heading hierarchy",
            "Optimize page load speed",
            "Ensure mobile responsiveness",
            "Fix broken links"
        ],
        'citations': [
            "Cite authoritative sources",
            "Link to official documentation",
            "Include expert quotes",
            "Reference recent research",
            "Add statistics from credible sources"
        ],
        'compliance': [
            "Avoid keyword stuffing",
            "No hidden text or cloaking",
            "Provide accurate information",
            "Include proper disclaimers",
            "Follow white-hat SEO practices"
        ]
    }
    
    if category:
        if category not in best_practices:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        return {
            'category': category,
            'practices': best_practices[category]
        }
    
    return {
        'categories': list(best_practices.keys()),
        'all_practices': best_practices
    }
