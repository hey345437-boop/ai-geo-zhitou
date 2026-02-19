"""
Business Impact Tracking API Endpoints

Provides endpoints for tracking business metrics, attribution analysis, and ROI calculation.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

from app.services.business_impact import (
    GA4Integration,
    CRMIntegration,
    AttributionAnalyzer,
    ROICalculator,
    BusinessMetric
)

router = APIRouter()

# Initialize services
ga4_integration = GA4Integration()
attribution_analyzer = AttributionAnalyzer()
roi_calculator = ROICalculator()


# Request/Response Models
class IntegrationConfigRequest(BaseModel):
    """Request model for integration configuration"""
    integration_type: str = Field(..., description="Type of integration (ga4, salesforce, hubspot)")
    credentials: Dict[str, str] = Field(..., description="Integration credentials")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional configuration")


class MetricSyncRequest(BaseModel):
    """Request model for syncing metrics"""
    integration_type: str
    start_date: datetime
    end_date: datetime
    metric_types: Optional[List[str]] = None


class AttributionRequest(BaseModel):
    """Request model for attribution analysis"""
    brand_id: str
    start_date: datetime
    end_date: datetime
    metric_type: str
    lookback_days: int = Field(30, ge=1, le=90, description="Lookback period in days")


class ROIRequest(BaseModel):
    """Request model for ROI calculation"""
    brand_id: str
    start_date: datetime
    end_date: datetime
    investment_amount: float = Field(..., gt=0, description="Total investment amount")


class IntegrationStatusResponse(BaseModel):
    """Response model for integration status"""
    integration_type: str
    status: str
    last_sync: Optional[datetime]
    metrics_count: int
    error: Optional[str]


class MetricDataResponse(BaseModel):
    """Response model for metric data"""
    metric_id: str
    brand_id: str
    metric_type: str
    value: float
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]


class AttributionResponse(BaseModel):
    """Response model for attribution analysis"""
    brand_id: str
    metric_type: str
    visibility_change: float
    metric_change: float
    correlation: float
    confidence_score: float
    time_lag_days: int
    analysis_period: Dict[str, datetime]


class ROIResponse(BaseModel):
    """Response model for ROI calculation"""
    brand_id: str
    investment: float
    revenue_impact: float
    roi_percentage: float
    payback_period_days: Optional[int]
    metrics_breakdown: Dict[str, float]
    analysis_period: Dict[str, datetime]


@router.post("/integrations/ga4/configure", response_model=IntegrationStatusResponse)
async def configure_ga4(request: IntegrationConfigRequest):
    """
    Configure Google Analytics 4 integration
    
    Sets up GA4 integration for tracking website traffic and user behavior metrics.
    """
    try:
        # Validate credentials
        if "property_id" not in request.credentials:
            raise HTTPException(status_code=400, detail="GA4 property_id is required")
        
        # In production, store credentials securely and test connection
        return IntegrationStatusResponse(
            integration_type="ga4",
            status="connected",
            last_sync=None,
            metrics_count=0,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure GA4: {str(e)}")


@router.post("/integrations/salesforce/configure", response_model=IntegrationStatusResponse)
async def configure_salesforce(request: IntegrationConfigRequest):
    """
    Configure Salesforce CRM integration
    
    Sets up Salesforce integration for tracking leads and conversion data.
    """
    try:
        # Validate credentials
        required_fields = ["instance_url", "access_token"]
        if not all(field in request.credentials for field in required_fields):
            raise HTTPException(status_code=400, detail="Salesforce credentials incomplete")
        
        # In production, store credentials and test connection
        return IntegrationStatusResponse(
            integration_type="salesforce",
            status="connected",
            last_sync=None,
            metrics_count=0,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure Salesforce: {str(e)}")


@router.post("/integrations/hubspot/configure", response_model=IntegrationStatusResponse)
async def configure_hubspot(request: IntegrationConfigRequest):
    """
    Configure HubSpot CRM integration
    
    Sets up HubSpot integration for tracking leads and marketing metrics.
    """
    try:
        # Validate credentials
        if "api_key" not in request.credentials:
            raise HTTPException(status_code=400, detail="HubSpot API key is required")
        
        # In production, store credentials and test connection
        return IntegrationStatusResponse(
            integration_type="hubspot",
            status="connected",
            last_sync=None,
            metrics_count=0,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure HubSpot: {str(e)}")


@router.post("/integrations/sync", response_model=Dict[str, Any])
async def sync_metrics(request: MetricSyncRequest):
    """
    Sync metrics from integrated platforms
    
    Fetches and stores business metrics from configured integrations.
    """
    try:
        # In production, fetch data from the integration
        synced_count = 0
        
        if request.integration_type == "ga4":
            # Mock GA4 sync
            synced_count = 100
        elif request.integration_type in ["salesforce", "hubspot"]:
            # Mock CRM sync
            synced_count = 50
        
        return {
            "integration_type": request.integration_type,
            "synced_count": synced_count,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync metrics: {str(e)}")


@router.get("/integrations/status", response_model=List[IntegrationStatusResponse])
async def get_integration_status():
    """
    Get status of all configured integrations
    
    Returns the connection status and last sync time for all integrations.
    """
    # In production, fetch from database
    return [
        IntegrationStatusResponse(
            integration_type="ga4",
            status="connected",
            last_sync=datetime.utcnow() - timedelta(hours=1),
            metrics_count=1500,
            error=None
        ),
        IntegrationStatusResponse(
            integration_type="salesforce",
            status="connected",
            last_sync=datetime.utcnow() - timedelta(hours=2),
            metrics_count=350,
            error=None
        ),
        IntegrationStatusResponse(
            integration_type="hubspot",
            status="disconnected",
            last_sync=datetime.utcnow() - timedelta(days=7),
            metrics_count=0,
            error="Authentication expired"
        )
    ]


@router.get("/metrics/{brand_id}", response_model=List[MetricDataResponse])
async def get_brand_metrics(
    brand_id: str,
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get business metrics for a brand
    
    Retrieves historical business metrics data for analysis.
    """
    # In production, fetch from database with filters
    # Mock data for demonstration
    metrics = []
    base_time = datetime.utcnow() - timedelta(days=30)
    
    for i in range(min(limit, 30)):
        metrics.append(MetricDataResponse(
            metric_id=f"metric_{i}",
            brand_id=brand_id,
            metric_type=metric_type or "traffic",
            value=1000 + i * 50,
            timestamp=base_time + timedelta(days=i),
            source="ga4",
            metadata={"page_views": 5000 + i * 100}
        ))
    
    return metrics


@router.post("/attribution/analyze", response_model=AttributionResponse)
async def analyze_attribution(request: AttributionRequest):
    """
    Analyze attribution between visibility and business metrics
    
    Correlates visibility changes with business metric changes to determine impact.
    """
    try:
        # Mock visibility data
        visibility_data = [
            {"timestamp": request.start_date + timedelta(days=i), "score": 50 + i * 2}
            for i in range((request.end_date - request.start_date).days)
        ]
        
        # Mock metric data
        metric_data = [
            {"timestamp": request.start_date + timedelta(days=i), "value": 1000 + i * 30}
            for i in range((request.end_date - request.start_date).days)
        ]
        
        # Calculate attribution
        result = impact_tracker.calculate_attribution(
            brand_id=request.brand_id,
            visibility_data=visibility_data,
            metric_data=metric_data,
            metric_type=MetricType(request.metric_type),
            lookback_days=request.lookback_days
        )
        
        return AttributionResponse(
            brand_id=request.brand_id,
            metric_type=request.metric_type,
            visibility_change=result.visibility_change,
            metric_change=result.metric_change,
            correlation=result.correlation,
            confidence_score=result.confidence_score,
            time_lag_days=result.time_lag_days,
            analysis_period={
                "start": request.start_date,
                "end": request.end_date
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze attribution: {str(e)}")


@router.post("/roi/calculate", response_model=ROIResponse)
async def calculate_roi(request: ROIRequest):
    """
    Calculate ROI from visibility improvements
    
    Estimates the return on investment based on visibility changes and business impact.
    """
    try:
        # Mock visibility improvement data
        visibility_improvement = 25.5  # 25.5% improvement
        
        # Mock metric improvements
        metric_improvements = {
            "traffic": 1500,
            "leads": 45,
            "conversions": 12
        }
        
        # Calculate ROI
        roi_report = impact_tracker.calculate_roi(
            brand_id=request.brand_id,
            visibility_improvement=visibility_improvement,
            metric_improvements=metric_improvements,
            investment=request.investment,
            time_period_days=(request.end_date - request.start_date).days
        )
        
        return ROIResponse(
            brand_id=request.brand_id,
            investment=request.investment,
            revenue_impact=roi_report.revenue_impact,
            roi_percentage=roi_report.roi_percentage,
            payback_period_days=roi_report.payback_period_days,
            metrics_breakdown=roi_report.metrics_breakdown,
            analysis_period={
                "start": request.start_date,
                "end": request.end_date
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate ROI: {str(e)}")


@router.get("/impact/summary/{brand_id}")
async def get_impact_summary(
    brand_id: str,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get comprehensive business impact summary
    
    Provides an overview of all business metrics and their relationship to visibility.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    return {
        "brand_id": brand_id,
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
            "days": days
        },
        "visibility": {
            "current_score": 75.5,
            "change": 15.2,
            "trend": "improving"
        },
        "metrics": {
            "traffic": {
                "current": 45000,
                "change": 8500,
                "change_percent": 23.3
            },
            "leads": {
                "current": 1250,
                "change": 280,
                "change_percent": 28.9
            },
            "conversions": {
                "current": 185,
                "change": 42,
                "change_percent": 29.4
            }
        },
        "attribution": {
            "correlation": 0.78,
            "confidence": 0.85,
            "time_lag_days": 7
        },
        "roi": {
            "estimated_revenue": 125000,
            "roi_percentage": 450,
            "payback_period_days": 45
        }
    }
