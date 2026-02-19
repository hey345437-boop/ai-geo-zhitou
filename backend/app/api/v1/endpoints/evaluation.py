"""
Evaluation Protocol API Endpoints

Provides endpoints for reproducible evaluation runs and drift monitoring.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.evaluation_protocol import (
    ReproducibleEvaluationProtocol,
    ModelDriftMonitor,
    EvaluationConfig,
    EvaluationStatus
)

router = APIRouter()
protocol = ReproducibleEvaluationProtocol()
drift_monitor = ModelDriftMonitor()


# Request/Response Models
class EvaluationRunRequest(BaseModel):
    """Request model for creating evaluation run"""
    question_set_name: str = Field(..., description="Question set name")
    question_set_version: str = Field(..., description="Question set version")
    engines: List[str] = Field(..., description="LLM engines to evaluate")
    sample_size: Optional[int] = Field(None, description="Sample size (None = all)")
    timeout_seconds: int = Field(300, ge=30, le=3600)
    max_retries: int = Field(3, ge=0, le=10)
    random_seed: int = Field(42, description="Random seed for reproducibility")
    parameters: Dict[str, Any] = Field(default_factory=dict)


class EvaluationRunResponse(BaseModel):
    """Response model for evaluation run"""
    run_id: str
    status: str
    config: Dict[str, Any]
    environment: Dict[str, Any]
    started_at: str
    completed_at: Optional[str]
    metrics: Dict[str, float]
    result_count: int


class ReproduceRequest(BaseModel):
    """Request model for reproducing evaluation"""
    baseline_run_id: str = Field(..., description="Run ID to reproduce")


class DriftCheckRequest(BaseModel):
    """Request model for drift checking"""
    baseline_run_id: str = Field(..., description="Baseline run ID")
    current_run_id: str = Field(..., description="Current run ID")


@router.post("/evaluation/run", response_model=EvaluationRunResponse, status_code=201)
async def create_evaluation_run(request: EvaluationRunRequest):
    """
    Create and execute a new evaluation run
    
    Creates a reproducible evaluation run with captured environment
    and configuration.
    """
    try:
        # Create configuration
        config = EvaluationConfig(
            question_set_name=request.question_set_name,
            question_set_version=request.question_set_version,
            engines=request.engines,
            sample_size=request.sample_size,
            timeout_seconds=request.timeout_seconds,
            max_retries=request.max_retries,
            parameters=request.parameters
        )
        
        # Create evaluation run
        run = protocol.create_evaluation_run(config, request.random_seed)
        
        # Mock question set for execution
        question_set = [
            {
                'id': f'q{i}',
                'text': f'Sample question {i}',
                'intent': 'informational'
            }
            for i in range(request.sample_size or 10)
        ]
        
        # Execute evaluation
        run = protocol.execute_evaluation(run, question_set)
        
        return EvaluationRunResponse(
            run_id=run.run_id,
            status=run.status.value,
            config=run.config.to_dict(),
            environment=run.environment.to_dict(),
            started_at=run.started_at.isoformat() if run.started_at else "",
            completed_at=run.completed_at.isoformat() if run.completed_at else None,
            metrics=run.metrics,
            result_count=len(run.results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create evaluation run: {str(e)}")


@router.get("/evaluation/{run_id}", response_model=Dict[str, Any])
async def get_evaluation_run(run_id: str):
    """
    Get evaluation run details
    
    Retrieves complete information about an evaluation run including
    results and metrics.
    """
    run = protocol.runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Evaluation run {run_id} not found")
    
    return run.to_dict()


@router.get("/evaluation", response_model=List[Dict[str, Any]])
async def list_evaluation_runs(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100)
):
    """
    List all evaluation runs
    
    Returns a list of evaluation runs with optional filtering.
    """
    runs = list(protocol.runs.values())
    
    # Filter by status if provided
    if status:
        try:
            status_enum = EvaluationStatus(status)
            runs = [r for r in runs if r.status == status_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    # Sort by creation time (newest first)
    runs.sort(key=lambda r: r.started_at or datetime.min, reverse=True)
    
    # Limit results
    runs = runs[:limit]
    
    return [
        {
            'run_id': r.run_id,
            'status': r.status.value,
            'question_set': r.config.question_set_name,
            'engines': r.config.engines,
            'started_at': r.started_at.isoformat() if r.started_at else None,
            'completed_at': r.completed_at.isoformat() if r.completed_at else None,
            'metrics': r.metrics
        }
        for r in runs
    ]


@router.post("/evaluation/reproduce", response_model=EvaluationRunResponse)
async def reproduce_evaluation(request: ReproduceRequest):
    """
    Reproduce a previous evaluation run
    
    Re-runs an evaluation with the same configuration and random seed
    to verify reproducibility.
    """
    try:
        # Mock question set
        question_set = [
            {
                'id': f'q{i}',
                'text': f'Sample question {i}',
                'intent': 'informational'
            }
            for i in range(10)
        ]
        
        # Reproduce evaluation
        reproduced_run = protocol.reproduce_evaluation(
            request.baseline_run_id,
            question_set
        )
        
        return EvaluationRunResponse(
            run_id=reproduced_run.run_id,
            status=reproduced_run.status.value,
            config=reproduced_run.config.to_dict(),
            environment=reproduced_run.environment.to_dict(),
            started_at=reproduced_run.started_at.isoformat() if reproduced_run.started_at else "",
            completed_at=reproduced_run.completed_at.isoformat() if reproduced_run.completed_at else None,
            metrics=reproduced_run.metrics,
            result_count=len(reproduced_run.results)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reproduce evaluation: {str(e)}")


@router.post("/evaluation/compare")
async def compare_evaluations(
    run_id_1: str = Query(..., description="First run ID"),
    run_id_2: str = Query(..., description="Second run ID")
):
    """
    Compare two evaluation runs
    
    Compares metrics and calculates reproducibility score between two runs.
    """
    try:
        comparison = protocol.compare_runs(run_id_1, run_id_2)
        return comparison
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compare runs: {str(e)}")


@router.post("/evaluation/drift/check")
async def check_drift(request: DriftCheckRequest):
    """
    Check for model drift
    
    Compares current run against baseline to detect significant drift
    in model behavior.
    """
    try:
        baseline_run = protocol.runs.get(request.baseline_run_id)
        current_run = protocol.runs.get(request.current_run_id)
        
        if not baseline_run:
            raise HTTPException(
                status_code=404,
                detail=f"Baseline run {request.baseline_run_id} not found"
            )
        if not current_run:
            raise HTTPException(
                status_code=404,
                detail=f"Current run {request.current_run_id} not found"
            )
        
        # Detect drift
        drift_report = drift_monitor.detect_drift(baseline_run, current_run)
        
        return drift_report.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check drift: {str(e)}")


@router.get("/evaluation/drift/history")
async def get_drift_history(
    baseline_run_id: str = Query(..., description="Baseline run ID"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get drift history for a baseline
    
    Returns drift reports comparing the baseline against recent runs.
    """
    baseline_run = protocol.runs.get(baseline_run_id)
    if not baseline_run:
        raise HTTPException(
            status_code=404,
            detail=f"Baseline run {baseline_run_id} not found"
        )
    
    # Get recent runs (excluding baseline)
    recent_runs = [
        r for r in protocol.runs.values()
        if r.run_id != baseline_run_id and r.status == EvaluationStatus.COMPLETED
    ]
    recent_runs.sort(key=lambda r: r.started_at or datetime.min, reverse=True)
    recent_runs = recent_runs[:limit]
    
    # Calculate drift for each
    drift_history = []
    for run in recent_runs:
        try:
            drift_report = drift_monitor.detect_drift(baseline_run, run)
            drift_history.append({
                'current_run_id': run.run_id,
                'checked_at': drift_report.checked_at.isoformat(),
                'overall_drift_score': drift_report.overall_drift_score,
                'has_significant_drift': drift_report.has_significant_drift,
                'drift_metrics_count': len(drift_report.drift_metrics)
            })
        except Exception:
            continue
    
    return {
        'baseline_run_id': baseline_run_id,
        'drift_history': drift_history
    }


@router.get("/evaluation/metrics/summary")
async def get_metrics_summary(
    question_set_name: Optional[str] = Query(None, description="Filter by question set"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get evaluation metrics summary
    
    Provides aggregate statistics across evaluation runs.
    """
    # Filter runs
    runs = list(protocol.runs.values())
    
    if question_set_name:
        runs = [
            r for r in runs
            if r.config.question_set_name == question_set_name
        ]
    
    # Filter by date
    cutoff_date = datetime.utcnow().timestamp() - (days * 86400)
    runs = [
        r for r in runs
        if r.started_at and r.started_at.timestamp() > cutoff_date
    ]
    
    if not runs:
        return {
            'total_runs': 0,
            'avg_metrics': {},
            'trend': 'insufficient_data'
        }
    
    # Calculate averages
    metric_names = set()
    for run in runs:
        metric_names.update(run.metrics.keys())
    
    avg_metrics = {}
    for metric_name in metric_names:
        values = [
            run.metrics[metric_name]
            for run in runs
            if metric_name in run.metrics
        ]
        if values:
            avg_metrics[metric_name] = round(sum(values) / len(values), 2)
    
    # Determine trend (simple: compare first half vs second half)
    mid_point = len(runs) // 2
    if mid_point > 0:
        first_half_avg = sum(
            r.metrics.get('avg_visibility_score', 0)
            for r in runs[:mid_point]
        ) / mid_point
        second_half_avg = sum(
            r.metrics.get('avg_visibility_score', 0)
            for r in runs[mid_point:]
        ) / (len(runs) - mid_point)
        
        if second_half_avg > first_half_avg * 1.05:
            trend = 'improving'
        elif second_half_avg < first_half_avg * 0.95:
            trend = 'declining'
        else:
            trend = 'stable'
    else:
        trend = 'insufficient_data'
    
    return {
        'total_runs': len(runs),
        'avg_metrics': avg_metrics,
        'trend': trend,
        'period_days': days
    }
