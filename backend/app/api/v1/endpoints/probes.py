from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import logging

from app.services.probe_service import probe_scheduler

router = APIRouter()
logger = logging.getLogger(__name__)


class ProbeRequest(BaseModel):
    brand: str
    keywords: List[str]
    frequency: str = "daily"
    llm_engines: List[str] = ["gpt-4", "claude-3", "gemini-pro"]


class ProbeResponse(BaseModel):
    id: str
    brand: str
    keywords: List[str]
    frequency: str
    llm_engines: List[str]
    status: str
    next_run_at: str


@router.post("/create", response_model=ProbeResponse)
async def create_probe(request: ProbeRequest):
    """
    Create a new probe job
    """
    try:
        job = await probe_scheduler.create_probe(
            brand=request.brand,
            keywords=request.keywords,
            frequency=request.frequency,
            llm_engines=request.llm_engines
        )
        
        return ProbeResponse(**job)
        
    except Exception as e:
        logger.error(f"Failed to create probe: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{job_id}/execute")
async def execute_probe(job_id: str):
    """
    Execute a probe job immediately
    """
    try:
        result = await probe_scheduler.execute_probe(job_id)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to execute probe: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/results")
async def get_probe_results(job_id: str, timeframe: str = "30d"):
    """
    Get probe results for a job
    """
    try:
        results = probe_scheduler.get_probe_results(job_id, timeframe)
        return results
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get probe results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_probes():
    """
    List all probe jobs
    """
    try:
        probes = probe_scheduler.list_probes()
        return {"probes": probes, "total": len(probes)}
        
    except Exception as e:
        logger.error(f"Failed to list probes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
