"""
Cost Control API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from app.services.cost_controller import (
    cost_tracker,
    CostOptimizer,
    UserTier,
    BudgetStatus
)

router = APIRouter()


class BudgetStatusResponse(BaseModel):
    """Budget status response"""
    tier: str
    monthly_limit: float
    monthly_used: float
    monthly_remaining: float
    daily_used: float
    daily_remaining: float
    is_exceeded: bool
    warning_level: str


class CostBreakdownResponse(BaseModel):
    """Cost breakdown response"""
    total_cost: float
    breakdown_by_engine: Dict[str, float]
    period_days: int


class CostForecastResponse(BaseModel):
    """Cost forecast response"""
    current_monthly_cost: float
    forecasted_monthly_cost: float
    days_remaining: int


class UpdateBudgetRequest(BaseModel):
    """Request to update budget limit"""
    monthly_limit: float


class EstimateCostRequest(BaseModel):
    """Request to estimate query cost"""
    engine: str
    estimated_tokens: int


@router.get("/current-month", response_model=BudgetStatusResponse)
async def get_current_month_status(user_id: str = "default_user"):
    """Get current month budget status"""
    try:
        # Default to PRO tier for demo
        tier = UserTier.PRO
        status = cost_tracker.get_budget_status(user_id, tier)
        
        return BudgetStatusResponse(
            tier=status.tier.value,
            monthly_limit=status.monthly_limit,
            monthly_used=status.monthly_used,
            monthly_remaining=status.monthly_remaining,
            daily_used=status.daily_used,
            daily_remaining=status.daily_remaining,
            is_exceeded=status.is_exceeded,
            warning_level=status.warning_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/breakdown", response_model=CostBreakdownResponse)
async def get_cost_breakdown(
    user_id: str = "default_user",
    days: int = 30
):
    """Get cost breakdown by engine"""
    try:
        breakdown = cost_tracker.get_cost_breakdown(user_id, days)
        total_cost = sum(breakdown.values())
        
        return CostBreakdownResponse(
            total_cost=total_cost,
            breakdown_by_engine=breakdown,
            period_days=days
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast", response_model=CostForecastResponse)
async def get_cost_forecast(user_id: str = "default_user"):
    """Get forecasted monthly cost"""
    try:
        current_cost = cost_tracker.get_monthly_cost(user_id)
        forecast = cost_tracker.forecast_monthly_cost(user_id)
        
        from datetime import datetime, timedelta
        now = datetime.now()
        next_month = datetime(now.year, now.month + 1, 1)
        days_remaining = (next_month - now).days
        
        return CostForecastResponse(
            current_monthly_cost=current_cost,
            forecasted_monthly_cost=forecast,
            days_remaining=days_remaining
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/estimate")
async def estimate_query_cost(request: EstimateCostRequest):
    """Estimate cost before query execution"""
    try:
        estimated_cost = CostOptimizer.estimate_cost(
            request.engine,
            request.estimated_tokens
        )
        
        return {
            "engine": request.engine,
            "estimated_tokens": request.estimated_tokens,
            "estimated_cost": estimated_cost,
            "currency": "USD"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-budget")
async def check_budget(
    user_id: str = "default_user",
    estimated_cost: float = 0.0
):
    """Check if user has budget for query"""
    try:
        tier = UserTier.PRO  # Default tier
        allowed, message = cost_tracker.check_budget(user_id, tier, estimated_cost)
        
        return {
            "allowed": allowed,
            "message": message,
            "estimated_cost": estimated_cost
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimize-engines")
async def optimize_engine_selection(
    budget: float,
    estimated_tokens: int = 1000
):
    """Get list of engines within budget"""
    try:
        all_engines = list(CostOptimizer.ENGINE_COSTS.keys())
        affordable_engines = CostOptimizer.optimize_query_cost(
            all_engines,
            budget,
            estimated_tokens
        )
        
        return {
            "budget": budget,
            "estimated_tokens": estimated_tokens,
            "affordable_engines": affordable_engines,
            "total_engines": len(affordable_engines)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
