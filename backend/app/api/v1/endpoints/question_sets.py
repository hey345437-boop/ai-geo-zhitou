"""
Question Set API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from app.services.question_set_manager import (
    question_set_manager,
    BenchmarkQuestionSets,
    Question,
    EvaluationConfig,
    QuestionSet
)

router = APIRouter()


class QuestionModel(BaseModel):
    """Question model"""
    id: str
    text: str
    intent_type: str
    category: str
    language: str = "en"
    metadata: Dict = {}


class EvaluationConfigModel(BaseModel):
    """Evaluation config model"""
    engines: List[str]
    temperature: float = 0.7
    max_tokens: int = 1000
    seed: Optional[int] = 42
    region: Optional[str] = None
    language: Optional[str] = "en"


class CreateQuestionSetRequest(BaseModel):
    """Request to create question set"""
    name: str
    questions: List[QuestionModel]
    evaluation_config: EvaluationConfigModel
    description: str = ""
    tags: List[str] = []


class QuestionSetResponse(BaseModel):
    """Question set response"""
    name: str
    version: str
    created_at: datetime
    description: str
    tags: List[str]
    total_questions: int
    commit_hash: Optional[str]


class CompareVersionsResponse(BaseModel):
    """Version comparison response"""
    name: str
    version1: str
    version2: str
    questions: Dict
    evaluation_config_changed: bool
    config_diff: Optional[Dict]


@router.post("/create", response_model=QuestionSetResponse)
async def create_question_set(request: CreateQuestionSetRequest):
    """Create a new question set"""
    try:
        # Convert models to domain objects
        questions = [
            Question(
                id=q.id,
                text=q.text,
                intent_type=q.intent_type,
                category=q.category,
                language=q.language,
                metadata=q.metadata
            )
            for q in request.questions
        ]
        
        eval_config = EvaluationConfig(
            engines=request.evaluation_config.engines,
            temperature=request.evaluation_config.temperature,
            max_tokens=request.evaluation_config.max_tokens,
            seed=request.evaluation_config.seed,
            region=request.evaluation_config.region,
            language=request.evaluation_config.language
        )
        
        # Create question set
        question_set = question_set_manager.create_question_set(
            name=request.name,
            questions=questions,
            evaluation_config=eval_config,
            description=request.description,
            tags=request.tags
        )
        
        return QuestionSetResponse(
            name=question_set.name,
            version=question_set.version,
            created_at=question_set.created_at,
            description=question_set.description,
            tags=question_set.tags,
            total_questions=len(question_set.questions),
            commit_hash=question_set.commit_hash
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{name}/versions")
async def list_versions(name: str):
    """List all versions of a question set"""
    try:
        versions = question_set_manager.list_versions(name)
        
        if not versions:
            raise HTTPException(status_code=404, detail=f"Question set '{name}' not found")
        
        return {
            "name": name,
            "versions": versions,
            "total_versions": len(versions),
            "latest_version": versions[-1] if versions else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{name}/{version}")
async def get_question_set(name: str, version: Optional[str] = None):
    """Get a specific question set version"""
    try:
        question_set = question_set_manager.get_question_set(name, version)
        
        if not question_set:
            raise HTTPException(
                status_code=404,
                detail=f"Question set '{name}' version '{version}' not found"
            )
        
        return {
            "name": question_set.name,
            "version": question_set.version,
            "created_at": question_set.created_at.isoformat(),
            "description": question_set.description,
            "tags": question_set.tags,
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "intent_type": q.intent_type,
                    "category": q.category,
                    "language": q.language
                }
                for q in question_set.questions
            ],
            "evaluation_config": {
                "engines": question_set.evaluation_config.engines,
                "temperature": question_set.evaluation_config.temperature,
                "max_tokens": question_set.evaluation_config.max_tokens,
                "seed": question_set.evaluation_config.seed
            },
            "commit_hash": question_set.commit_hash
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=CompareVersionsResponse)
async def compare_versions(
    name: str,
    version1: str,
    version2: str
):
    """Compare two versions of a question set"""
    try:
        comparison = question_set_manager.compare_versions(name, version1, version2)
        
        return CompareVersionsResponse(
            name=comparison["name"],
            version1=comparison["version1"],
            version2=comparison["version2"],
            questions=comparison["questions"],
            evaluation_config_changed=comparison["evaluation_config_changed"],
            config_diff=comparison.get("config_diff")
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/benchmarks/list")
async def list_benchmarks():
    """List available benchmark question sets"""
    return {
        "benchmarks": [
            {
                "name": "ecommerce",
                "description": "E-commerce product search and comparison",
                "total_questions": 5,
                "categories": ["electronics", "food", "sports", "policy"]
            },
            {
                "name": "local_business",
                "description": "Local business search queries",
                "total_questions": 5,
                "categories": ["restaurant", "healthcare", "automotive", "pharmacy", "cafe"]
            },
            {
                "name": "saas",
                "description": "SaaS product comparison and features",
                "total_questions": 5,
                "categories": ["productivity", "integration", "crm", "finance", "communication"]
            }
        ]
    }


@router.post("/benchmarks/{benchmark_name}/create")
async def create_benchmark_question_set(benchmark_name: str):
    """Create a question set from a benchmark"""
    try:
        # Get benchmark questions
        if benchmark_name == "ecommerce":
            questions = BenchmarkQuestionSets.create_ecommerce_benchmark()
        elif benchmark_name == "local_business":
            questions = BenchmarkQuestionSets.create_local_business_benchmark()
        elif benchmark_name == "saas":
            questions = BenchmarkQuestionSets.create_saas_benchmark()
        else:
            raise HTTPException(status_code=404, detail=f"Benchmark '{benchmark_name}' not found")
        
        # Create default evaluation config
        eval_config = EvaluationConfig(
            engines=["gpt-4", "claude-3", "gemini-pro", "perplexity"],
            temperature=0.7,
            max_tokens=1000,
            seed=42
        )
        
        # Create question set
        question_set = question_set_manager.create_question_set(
            name=f"benchmark_{benchmark_name}",
            questions=questions,
            evaluation_config=eval_config,
            description=f"Benchmark question set for {benchmark_name}",
            tags=["benchmark", benchmark_name]
        )
        
        return {
            "name": question_set.name,
            "version": question_set.version,
            "total_questions": len(question_set.questions),
            "message": f"Benchmark '{benchmark_name}' created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
