"""
Multi-Armed Bandit API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from app.services.multi_armed_bandit import (
    thompson_sampling,
    contextual_bandit,
    BanditContext
)

router = APIRouter()


class AddArmRequest(BaseModel):
    arm_id: str
    name: str
    description: str
    cost: float = 0.0


class SelectArmRequest(BaseModel):
    context: Optional[Dict] = None
    budget_constraint: Optional[float] = None


class UpdateRewardRequest(BaseModel):
    arm_id: str
    reward: float
    cost: float = 0.0
    context: Optional[Dict] = None


@router.post("/add-arm")
async def add_arm(request: AddArmRequest):
    """Add a new arm to the bandit"""
    try:
        arm = thompson_sampling.add_arm(
            arm_id=request.arm_id,
            name=request.name,
            description=request.description,
            cost=request.cost
        )
        
        return {
            "arm_id": arm.id,
            "name": arm.name,
            "description": arm.description,
            "cost": arm.cost,
            "created_at": arm.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/select-arm")
async def select_arm(request: SelectArmRequest):
    """Select arm using Thompson Sampling"""
    try:
        context = BanditContext(**request.context) if request.context else None
        
        selected_arm_id = thompson_sampling.select_arm(
            context=context,
            budget_constraint=request.budget_constraint
        )
        
        return {
            "selected_arm_id": selected_arm_id,
            "context": request.context,
            "budget_constraint": request.budget_constraint
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-reward")
async def update_reward(request: UpdateRewardRequest):
    """Update arm with observed reward"""
    try:
        context = BanditContext(**request.context) if request.context else None
        
        thompson_sampling.update(
            arm_id=request.arm_id,
            reward=request.reward,
            cost=request.cost,
            context=context
        )
        
        stats = thompson_sampling.get_arm_statistics(request.arm_id)
        
        return {
            "message": "Reward updated successfully",
            "arm_statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_performance():
    """Get overall bandit performance"""
    try:
        summary = thompson_sampling.get_performance_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/arm/{arm_id}/statistics")
async def get_arm_statistics(arm_id: str):
    """Get statistics for specific arm"""
    try:
        stats = thompson_sampling.get_arm_statistics(arm_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
