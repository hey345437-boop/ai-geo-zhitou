from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import logging
from datetime import datetime, timedelta
import random

router = APIRouter()
logger = logging.getLogger(__name__)


class ExperimentRequest(BaseModel):
    name: str
    hypothesis: str
    treatment: Dict
    control: Dict
    sample_size: int
    duration_days: int


@router.post("/create")
async def create_experiment(request: ExperimentRequest):
    """
    Create a new A/B experiment
    """
    try:
        experiment_id = f"exp-{random.randint(1000, 9999)}"
        start_date = datetime.now()
        end_date = start_date + timedelta(days=request.duration_days)
        
        logger.info(f"Created experiment: {experiment_id}")
        
        return {
            "experiment_id": experiment_id,
            "name": request.name,
            "status": "running",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "sample_size": request.sample_size
        }
        
    except Exception as e:
        logger.error(f"Failed to create experiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{experiment_id}/results")
async def get_experiment_results(experiment_id: str):
    """
    Get experiment results with causal analysis
    """
    try:
        # Simulate experiment results
        ate = random.uniform(0.10, 0.25)  # Average Treatment Effect
        p_value = random.uniform(0.001, 0.05)
        
        result = {
            "experiment_id": experiment_id,
            "status": "completed",
            "causal_effect": {
                "ate": round(ate, 3),
                "p_value": round(p_value, 4),
                "confidence_interval": [
                    round(ate - 0.05, 3),
                    round(ate + 0.05, 3)
                ],
                "is_significant": p_value < 0.05,
                "effect_size": "medium" if ate > 0.15 else "small"
            },
            "metrics": {
                "treatment_mean": round(0.75 + ate, 3),
                "control_mean": 0.75,
                "improvement": f"{round(ate * 100, 1)}%"
            },
            "recommendation": "Adopt treatment version" if p_value < 0.05 else "Continue testing"
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get experiment results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_experiments():
    """List all experiments"""
    return {
        "experiments": [
            {
                "id": "exp-1001",
                "name": "Title Optimization Test",
                "status": "running",
                "start_date": datetime.now().isoformat()
            }
        ],
        "total": 1
    }
