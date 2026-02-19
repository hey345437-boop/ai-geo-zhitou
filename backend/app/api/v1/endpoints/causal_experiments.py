"""
Causal Experiment API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from app.services.causal_experiment import (
    causal_experiment,
    ExperimentPlan,
    ExperimentStatus
)

router = APIRouter()


class DesignExperimentRequest(BaseModel):
    """Request to design experiment"""
    name: str
    hypothesis: str
    treatment_variant: str
    control_variant: str
    baseline_rate: float
    mde: float = 0.05
    alpha: float = 0.05
    power: float = 0.80
    duration_days: int = 14


class RunExperimentRequest(BaseModel):
    """Request to run experiment"""
    experiment_id: str
    treatment_data: List[Dict]
    control_data: List[Dict]


class DiDRequest(BaseModel):
    """Difference-in-Differences request"""
    treatment_before: List[float]
    treatment_after: List[float]
    control_before: List[float]
    control_after: List[float]


class PSMRequest(BaseModel):
    """Propensity Score Matching request"""
    treatment_units: List[Dict]
    control_units: List[Dict]
    covariates: List[str]


@router.post("/design")
async def design_experiment(request: DesignExperimentRequest):
    """Design a new experiment with power analysis"""
    try:
        plan = causal_experiment.design_experiment(
            name=request.name,
            hypothesis=request.hypothesis,
            treatment_variant=request.treatment_variant,
            control_variant=request.control_variant,
            baseline_rate=request.baseline_rate,
            mde=request.mde,
            alpha=request.alpha,
            power=request.power,
            duration_days=request.duration_days
        )
        
        return {
            "experiment_id": plan.id,
            "name": plan.name,
            "description": plan.description,
            "hypothesis": plan.hypothesis,
            "sample_size_per_group": plan.sample_size,
            "duration_days": plan.duration_days,
            "status": plan.status.value,
            "created_at": plan.created_at.isoformat(),
            "metadata": plan.metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run")
async def run_experiment(request: RunExperimentRequest):
    """Execute experiment and analyze results"""
    try:
        result = causal_experiment.run_experiment(
            experiment_id=request.experiment_id,
            treatment_data=request.treatment_data,
            control_data=request.control_data
        )
        
        return {
            "experiment_id": result.experiment_id,
            "treatment_group": result.treatment_group,
            "control_group": result.control_group,
            "causal_effect": {
                "ate": result.causal_effect.ate,
                "ci_lower": result.causal_effect.ate_ci_lower,
                "ci_upper": result.causal_effect.ate_ci_upper,
                "p_value": result.causal_effect.p_value,
                "is_significant": result.causal_effect.is_significant,
                "effect_size": result.causal_effect.effect_size,
                "relative_lift": result.causal_effect.relative_lift
            },
            "completed_at": result.completed_at.isoformat(),
            "sample_size_actual": result.sample_size_actual
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{experiment_id}/status")
async def get_experiment_status(experiment_id: str):
    """Get experiment status"""
    try:
        plan = causal_experiment.experiments.get(experiment_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail="Experiment not found")
        
        return {
            "experiment_id": plan.id,
            "name": plan.name,
            "status": plan.status.value,
            "created_at": plan.created_at.isoformat(),
            "duration_days": plan.duration_days,
            "sample_size": plan.sample_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{experiment_id}/results")
async def get_experiment_results(experiment_id: str):
    """Get experiment results"""
    try:
        result = causal_experiment.results.get(experiment_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Results not found")
        
        return {
            "experiment_id": result.experiment_id,
            "treatment_group": result.treatment_group,
            "control_group": result.control_group,
            "causal_effect": {
                "ate": result.causal_effect.ate,
                "ci_lower": result.causal_effect.ate_ci_lower,
                "ci_upper": result.causal_effect.ate_ci_upper,
                "p_value": result.causal_effect.p_value,
                "is_significant": result.causal_effect.is_significant,
                "effect_size": result.causal_effect.effect_size,
                "relative_lift": result.causal_effect.relative_lift
            },
            "completed_at": result.completed_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/did")
async def difference_in_differences(request: DiDRequest):
    """Perform Difference-in-Differences analysis"""
    try:
        result = causal_experiment.difference_in_differences(
            treatment_before=request.treatment_before,
            treatment_after=request.treatment_after,
            control_before=request.control_before,
            control_after=request.control_after
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/psm")
async def propensity_score_matching(request: PSMRequest):
    """Perform Propensity Score Matching"""
    try:
        matches, ate = causal_experiment.propensity_score_matching(
            treatment_units=request.treatment_units,
            control_units=request.control_units,
            covariates=request.covariates
        )
        
        return {
            "matched_pairs": len(matches),
            "ate": round(ate, 4),
            "matches": [
                {"treatment_idx": t_idx, "control_idx": c_idx}
                for t_idx, c_idx in matches[:100]  # Limit to first 100
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_experiments():
    """List all experiments"""
    try:
        experiments = []
        
        for exp_id, plan in causal_experiment.experiments.items():
            experiments.append({
                "experiment_id": plan.id,
                "name": plan.name,
                "status": plan.status.value,
                "created_at": plan.created_at.isoformat(),
                "has_results": exp_id in causal_experiment.results
            })
        
        return {
            "total": len(experiments),
            "experiments": experiments
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
